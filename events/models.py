from django.db import models

# Create your models here.
class Participant(models.Model):
    participant_name = models.CharField(max_length=100, null=False)
    participant_email = models.EmailField(null=False)
    registered_event = models.ManyToManyField("Event", related_name="registered_event")

class Category(models.Model):
    TODAY = "TODAY"
    UPCOMING = "UPCOMING"
    PAST = "PAST"

    EVENT_CATEGORY = (
        (TODAY, "Today's Event"),
        (UPCOMING, "Upcoming Event"),
        (PAST, 'Past Event')
    )

    category_name = models.CharField(max_length=50, choices=EVENT_CATEGORY, null=False, default=TODAY)
    category_description = models.TextField()

class Event(models.Model):
    name = models.CharField(max_length=100, null=False)
    description = models.TextField(null=False)
    date = models.DateField(blank=False, null=False)
    time = models.CharField(max_length=50, blank=False, null=False)
    location = models.CharField(max_length=100, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category")


