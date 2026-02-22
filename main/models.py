from django.db import models
from django.contrib.auth.models import User

class CustomHabit(models.Model):
    """
    The user's personal additions (e.g., Custom Zikr, Hadith reading).
    If they delete this, it stops generating for TOMORROW, but past days 
    keep their history because past days use flat copies in TodoItem.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='custom_habits')
    title = models.CharField(max_length=255)
    
    # 10=Tahajjud, 20=Fajr. So if they want this after Fajr, they set sort_order=25.
    sort_order = models.PositiveIntegerField() 
    
    # 0 for a simple checkbox. 100 for a 100-tap zikr counter.
    target_value = models.PositiveIntegerField(default=0) 

    def __str__(self):
        return f"{self.title} - {self.user.username}"


class DayLog(models.Model):
    """
    Created on the fly when the user logs in for the day.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='day_logs')
    date = models.DateField()
    fast_kept = models.BooleanField(default=False)

    class Meta:
        # A user can only have one log per specific date
        unique_together = ['user', 'date'] 

    def __str__(self):
        return f"{self.user.username} - {self.date}"


class TodoItem(models.Model):
    """
    The actual checklist items for a specific day. 
    Notice it does NOT link to CustomHabit. It's just a flat copy.
    """
    day_log = models.ForeignKey(DayLog, on_delete=models.CASCADE, related_name='todos')
    title = models.CharField(max_length=255)
    sort_order = models.PositiveIntegerField() 
    
    is_completed = models.BooleanField(default=False)
    with_jamaat = models.BooleanField(default=False) 
    
    target_value = models.PositiveIntegerField(default=0) 
    current_value = models.PositiveIntegerField(default=0) 
    
    text_input = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ['sort_order']

    def __str__(self):
        return f"{self.title} for {self.day_log}"