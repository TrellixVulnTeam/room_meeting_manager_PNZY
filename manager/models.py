from django.db import models

# Create your models here.


class MeetingRoom(models.Model):
    name = models.CharField(max_length=255, unique=True)
    seats = models.IntegerField()
    projector = models.BooleanField()
