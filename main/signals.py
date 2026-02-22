from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils import timezone
from .models import DayLog, TodoItem, CustomHabit

# HARDCODED DEFAULTS
# You don't need these in the database. Just keep them here!
DEFAULT_TASKS = [
    {'title': 'Tahajjud', 'order': 10, 'target': 8}, # Units (Rakahs)
    {'title': 'Suhoor (Sehri)', 'order': 15, 'target': 0},
    {'title': 'Fajr', 'order': 20, 'target': 0},
    {'title': 'Ishraq', 'order': 30, 'target': 0},
    {'title': 'Chasht (Duha)', 'order': 40, 'target': 0},
    {'title': 'Dhuhr', 'order': 50, 'target': 0},
    {'title': 'Asr', 'order': 60, 'target': 0},
    {'title': 'Maghrib', 'order': 70, 'target': 0},
    {'title': 'Isha', 'order': 80, 'target': 0},
    {'title': 'Taraweeh', 'order': 90, 'target': 20}, # Units (Rakahs)
    {'title': 'Quran Recitation', 'order': 100, 'target': 0}, # Text input
    {'title': 'Darood Shareef', 'order': 110, 'target': 100}, # Zikr counter
    {'title': 'Istighfar', 'order': 120, 'target': 100}, # Zikr counter
]

@receiver(user_logged_in)
def generate_daily_checklist(sender, request, user, **kwargs):
    today = timezone.localdate()
    
    # Check if a log already exists for today. If yes, do nothing.
    if DayLog.objects.filter(user=user, date=today).exists():
        return

    # 1. Create the new DayLog for today
    day_log = DayLog.objects.create(user=user, date=today)
    
    items_to_create = []

    # 2. Add all the hardcoded default tasks
    for task in DEFAULT_TASKS:
        items_to_create.append(
            TodoItem(
                day_log=day_log,
                title=task['title'],
                sort_order=task['order'],
                target_value=task['target']
            )
        )

    # 3. Add the user's custom habits
    custom_habits = CustomHabit.objects.filter(user=user)
    for habit in custom_habits:
        items_to_create.append(
            TodoItem(
                day_log=day_log,
                title=habit.title,
                sort_order=habit.sort_order,
                target_value=habit.target_value
            )
        )

    # 4. Save everything to the database in one single, fast hit
    TodoItem.objects.bulk_create(items_to_create)