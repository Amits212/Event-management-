from django.db import models
from django.urls import reverse
from datetime import datetime, timedelta
from django.utils import timezone

class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    venue = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    popularity = models.IntegerField()
    creation_time = models.DateTimeField(blank=True, null=True)

    @property
    def get_html_url(self):
        url = reverse('app:event_edit', args=[self.id])
        return f'<a href="{url}"> {self.title} </a>'

    @property
    def time_diff(self):
        event_time = timezone.localtime(self.start_time)
        current_time = timezone.localtime(timezone.now())
        time_diff = (event_time - current_time).total_seconds() / 60  # calculating time difference in minutes
        return 0 <= time_diff <= 30
