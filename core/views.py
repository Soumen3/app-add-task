from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import App, Task
from .serializers import AppSerializer, TaskSerializer
from .serializers import UserRegisterSerializer
from rest_framework.permissions import AllowAny
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json


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
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_task(request):
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Get user profile with tasks and points
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    user = request.user
    tasks = Task.objects.filter(user=user)
    total_points = sum([task.app.points for task in tasks if task.is_approved])
    serializer = TaskSerializer(tasks, many=True)
    return Response({
        "username": user.username,
        "email": user.email,
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
@login_required
def get_apps(request):
    apps = list(App.objects.values())
    return JsonResponse({"apps": apps})

# ✅ Create a new app
@csrf_exempt
@login_required
def create_app(request):
    if request.method == "POST":
        data = json.loads(request.body)
        app = App.objects.create(
            name=data["name"],
            link=data["link"],
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
@login_required
def delete_app(request, app_id):
    if request.method == "DELETE":
        try:
            app = App.objects.get(id=app_id)
            app.delete()
            return JsonResponse({"message": "App deleted successfully!"})
        except App.DoesNotExist:
            return JsonResponse({"error": "App not found"}, status=404)
