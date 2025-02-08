from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from .models import App, Task
from .serializers import AppSerializer, TaskSerializer
from .serializers import UserRegisterSerializer, UserLoginSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.middleware.csrf import get_token


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            token = get_tokens_for_user(user)
            return Response({'msg': 'User login successful', 'token': token, 'is_admin':user.is_staff}, status=status.HTTP_200_OK)
        else:
            return Response({'error': {'non_field_errors': ['Username or Password is not valid']}}, status=status.HTTP_401_UNAUTHORIZED)


# List all apps or create a new one
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def app_list(request):
    if request.method == 'GET':
        apps = App.objects.all()
        serializer = AppSerializer(apps, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = AppSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Upload task screenshot
@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_task(request, app_id):
    user = request.user
    screenshot = request.FILES.get('screenshot')
    app = get_object_or_404(App, id=app_id)
    task = Task.objects.create(user=user, app=app, screenshot=screenshot)
    serializer = TaskSerializer(task)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

# Get user profile with tasks and points
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    user = request.user
    tasks = Task.objects.filter(user=user)
    total_points = sum([task.app.points for task in tasks])
    serializer = TaskSerializer(tasks, many=True)
    return Response({
        "username": user.username,
        "email": user.email,
        'first_name':user.first_name,
        'last_name':user.last_name,
        "total_points": total_points,
        "tasks_completed": serializer.data,
        "is_admin": user.is_staff
    })


# User Registration View
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





# ✅ Get all apps (For Admin Dashboard)
# @login_required
@permission_classes([IsAuthenticated])
def get_apps(request):
    apps = list(App.objects.values())
    return JsonResponse({"apps": apps})

# ✅ Create a new app
@csrf_exempt
@permission_classes([IsAuthenticated])
def create_app(request):
    if request.method == "POST":
        data = json.loads(request.body)
        app = App.objects.create(
            name=data["name"],
            app_link=data["link"],
            category=data["category"],
            sub_category=data["sub_category"],
            points=data["points"]
        )
        return JsonResponse({"message": "App added successfully!", "app_id": app.id})

# ✅ Update an app
@csrf_exempt
@login_required
def update_app(request, app_id):
    if request.method == "PUT":
        data = json.loads(request.body)
        try:
            app = App.objects.get(id=app_id)
            app.name = data["name"]
            app.link = data["link"]
            app.category = data["category"]
            app.sub_category = data["sub_category"]
            app.points = data["points"]
            app.save()
            return JsonResponse({"message": "App updated successfully!"})
        except App.DoesNotExist:
            return JsonResponse({"error": "App not found"}, status=404)

# ✅ Delete an app
@csrf_exempt
@permission_classes([IsAuthenticated])
def delete_app(request, app_id):
    if request.method == "DELETE":
        try:
            app = App.objects.get(id=app_id)
            app.delete()
            return JsonResponse({"message": "App deleted successfully!"}, status=204)
        except App.DoesNotExist:
            return JsonResponse({"error": "App not found"}, status=404)


@permission_classes([IsAuthenticated])
def get_user_tasks(request, user):
    user = get_object_or_404(User, username=user)
    tasks = Task.objects.filter(user=user)
    serializer = TaskSerializer(tasks, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_undone_tasks(request, user):
    user = get_object_or_404(User, username=user)
    user_task_ids = Task.objects.filter(user=user).values_list('app_id', flat=True)
    undone_tasks = App.objects.exclude(id__in=user_task_ids)
    serializer = AppSerializer(undone_tasks, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})
