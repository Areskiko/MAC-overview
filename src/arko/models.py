from django.db import models
from django.utils import timezone
from datetime import datetime

class Device(models.Model):
    name = models.CharField(max_length=100)
    mac = models.CharField(max_length=17)
    ip = models.CharField(max_length=14, null=True)
    seenAgo = models.CharField(max_length=20, default=datetime.now())
    lastSeen = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.name