import django

from datetime import datetime, timezone

from django.db import models

from django.contrib.auth.models import User

period_choices = (
    (1, '1 hour'),
    (3, '3 hours'),
    (6, '6 hours'),
    (12, '12 hours'),
    (24, '24 hours'),
)


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=50)
    start_datetime = models.DateTimeField(default=django.utils.timezone.now)
    next_notification_datetime = models.DateTimeField()
    period_hours = models.IntegerField(choices=period_choices)

    def __str__(self):
        return f'{self.user.username} - {self.city}: {self.period_hours} hours, next at {self.next_notification_datetime}'
