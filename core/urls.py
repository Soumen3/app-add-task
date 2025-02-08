from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (app_list, upload_task, profile, register_user, get_apps, create_app, update_app, delete_app,
                    UserLoginView, get_user_tasks, user_undone_tasks, get_csrf_token)

urlpatterns = [
    path('register/', register_user, name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('apps/', app_list, name='app_list'),
    path('profile/', profile, name='profile'),
    path('tasks/<str:user>/', get_user_tasks, name='get_user_tasks'),
    path('tasks/undone/<str:user>/', user_undone_tasks, name='user_undone_tasks'),
    path('tasks/upload/<int:app_id>/', upload_task, name='upload_task'),
    path('csrf/', get_csrf_token, name='get_csrf_token'),

    path('admin/apps/', get_apps, name='get_apps'),
    path('admin/apps/create/', create_app, name='create_app'),
    path('admin/apps/update/<int:app_id>/', update_app, name='update_app'),
    path('admin/apps/delete/<int:app_id>/', delete_app, name='delete_app'),
]
