from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from .models import DayLog, TodoItem, CustomHabit

# --- 1. AUTHENTICATION ---
def register(request):
    """Simple registration that automatically logs the user in."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # The signal we wrote will fire here and build Day 1!
            return redirect('daily_checklist')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


# --- 2. MAIN DASHBOARD ---
@login_required
def daily_checklist(request):
    """Fetches today's checklist and the user's custom habits settings."""
    today = timezone.localdate()
    
    # Get today's log (created automatically by the login signal)
    day_log = DayLog.objects.filter(user=request.user, date=today).first()
    todos = day_log.todos.all() if day_log else []
    
    # Get their custom habits so they can see/delete them in a settings panel
    custom_habits = CustomHabit.objects.filter(user=request.user)
    
    context = {
        'day_log': day_log,
        'todos': todos,
        'custom_habits': custom_habits,
        'today': today
    }
    return render(request, 'checklist.html', context)


# --- 3. UPDATING TASKS (Checking off, Zikr counting) ---
@login_required
def update_todo(request, todo_id):
    """Handles checkmarks, zikr counter taps, and typing Quran progress."""
    if request.method == "POST":
        todo = get_object_or_404(TodoItem, id=todo_id, day_log__user=request.user)
        
        # Checkbox toggle
        if 'toggle' in request.POST:
            todo.is_completed = not todo.is_completed
            
        # Zikr counter tap
        elif 'increment' in request.POST:
            todo.current_value += 1
            if todo.target_value > 0 and todo.current_value >= todo.target_value:
                todo.is_completed = True # Auto-complete when target is hit
                
        # Typed input (e.g., "Read Juz 3")
        elif 'text_input' in request.POST:
            todo.text_input = request.POST.get('text_input')
            todo.is_completed = True
            
        todo.save()
    return redirect('daily_checklist')


# --- 4. ADD CUSTOM ZIKR/HABIT ---
@login_required
def add_custom_habit(request):
    """Saves a new habit and instantly adds it to today's list."""
    if request.method == "POST":
        title = request.POST.get('title')
        # Default to 100 (bottom of the list) if they don't specify where it goes
        sort_order = int(request.POST.get('sort_order', 100)) 
        target_value = int(request.POST.get('target_value', 0))
        
        # Save it to their custom template for future days
        habit = CustomHabit.objects.create(
            user=request.user,
            title=title,
            sort_order=sort_order,
            target_value=target_value
        )
        
        # Instantly add it to TODAY'S log so it shows up right now
        today = timezone.localdate()
        day_log = DayLog.objects.filter(user=request.user, date=today).first()
        if day_log:
            TodoItem.objects.create(
                day_log=day_log,
                title=habit.title,
                sort_order=habit.sort_order,
                target_value=habit.target_value
            )
            
    return redirect('daily_checklist')


# --- 5. DELETE CUSTOM HABIT ---
@login_required
def delete_custom_habit(request, habit_id):
    """Deletes a habit so it stops showing up tomorrow. (Preserves past history)."""
    if request.method == "POST":
        habit = get_object_or_404(CustomHabit, id=habit_id, user=request.user)
        habit.delete()
        
        # Optional: We don't delete today's copy here to keep things simple, 
        # it just won't generate tomorrow.
    return redirect('daily_checklist')