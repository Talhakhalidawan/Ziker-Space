from django.contrib import admin
from .models import CustomHabit, DayLog, TodoItem

admin.site.register(CustomHabit)
admin.site.register(DayLog)
admin.site.register(TodoItem)