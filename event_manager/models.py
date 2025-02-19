from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField()
    date = models.DateField()
    location = models.CharField(max_length=256)
    organizer = models.CharField(max_length=256)

