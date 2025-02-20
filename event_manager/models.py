from django.db import models


class Event(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField()
    date = models.DateField()
    location = models.CharField(max_length=256)
    organizer = models.ForeignKey("user.User" ,on_delete=models.CASCADE , related_name='event_user')
    members =  models.ManyToManyField("user.User", related_name="members")

