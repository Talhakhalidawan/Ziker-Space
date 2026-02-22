from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Auth URLs
    path('register/', views.register, name='register'),
    # Django's built-in login/logout handle the heavy lifting
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Core Dashboard
    path('', views.daily_checklist, name='daily_checklist'),
    path('update-todo/<int:todo_id>/', views.update_todo, name='update_todo'),
    
    # Custom Habit Management
    path('add-habit/', views.add_custom_habit, name='add_custom_habit'),
    path('delete-habit/<int:habit_id>/', views.delete_custom_habit, name='delete_custom_habit'),
]