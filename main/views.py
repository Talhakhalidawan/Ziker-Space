from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import DayLog, TodoItem

@login_required
def daily_checklist(request):
    """Fetches today's list for the logged-in user."""
    today = timezone.localdate()
    
    # The signal already created this when they logged in!
    day_log = DayLog.objects.filter(user=request.user, date=today).first()
    
    # Get all the tasks ordered by that magic sort_order number
    todos = day_log.todos.all() if day_log else []
    
    context = {
        'day_log': day_log,
        'todos': todos,
        'today': today
    }
    return render(request, 'checklist.html', context)


@login_required
def update_todo(request, todo_id):
    """Handles all updates: checkboxes, zikr taps, and text input."""
    if request.method == "POST":
        todo = get_object_or_404(TodoItem, id=todo_id, day_log__user=request.user)
        
        # 1. If it's a simple checkbox toggle (e.g., Fajr)
        if 'toggle' in request.POST:
            todo.is_completed = not todo.is_completed
            
        # 2. If it's a Zikr counter tap
        elif 'increment' in request.POST:
            todo.current_value += 1
            if todo.target_value > 0 and todo.current_value >= todo.target_value:
                todo.is_completed = True # Auto-complete when target reached
                
        # 3. If it's a text input (e.g., "Juz 3")
        elif 'text_input' in request.POST:
            todo.text_input = request.POST.get('text_input')
            todo.is_completed = True # Mark complete since they typed something
            
        todo.save()
        
    # Send them right back to the checklist
    return redirect('daily_checklist')