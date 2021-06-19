from django.db import models

# Create your models here.


class MeetingRoom(models.Model):
    name = models.CharField(max_length=255, unique=True)
    seats = models.IntegerField()
    projector = models.BooleanField()


class Reservation(models.Model):
    date = models.DateField()
    id_meeting_room = models.ForeignKey(MeetingRoom, on_delete=models.CASCADE)
    comment = models.TextField()

    class Meta:
        unique_together = ('date', 'id_meeting_room', )

