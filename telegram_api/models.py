from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Task(models.Model):
    telegram_id = models.BigIntegerField()
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField()
    completed = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.title
