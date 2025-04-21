from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class EventType(models.TextChoices):
    FOOTBALL = "Football", "Football"
    BASKETBALL = "Basketball", "Basketball"
    BOWLING = "Bowling", "Bowling"
    COMPUTER_CLUB = "Computer Club", "Computer Club"
    HIKING = "Hiking", "Hiking"

class Participant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='participant')
    age = models.SmallIntegerField()
    phoneNumber = models.CharField(max_length=11, unique=True)

    def __str__(self):
        return f"Name: {self.user.first_name} , Phone number: {self.phoneNumber}."
    
class Event(models.Model):
    type = models.CharField(max_length=20, choices=EventType.choices)
    place = models.TextField()
    date = models.DateTimeField()
    description = models.TextField()
    capacity = models.PositiveSmallIntegerField()
    isActive = models.BooleanField(default=True)
    creator = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name="created_events")


    def __str__(self):
        return f"{self.type} at {self.place} on {self.date}"

class EventParticipant(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    eventParticipants = models.ManyToManyField(Participant, related_name="joined_events", blank=True)
    
    def __str__(self):
        return f"joined event by {self.event.creator}"

    

class ListOfWaitingParticipant(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="event_participants")
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE ,related_name='waiting_participant')

    def __str__(self):
        return f"{self.participant} - waiting for {self.event}"