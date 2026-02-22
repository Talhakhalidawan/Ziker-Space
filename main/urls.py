from django.urls import path
from . import views

urlpatterns = [
    # The main page that shows the list
    path('', views.daily_checklist, name='daily_checklist'),
    
    # The invisible URL that processes button clicks and taps
    path('update-todo/<int:todo_id>/', views.update_todo, name='update_todo'),
]