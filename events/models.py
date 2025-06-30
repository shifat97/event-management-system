from django.db import models

# Create your models here.
class Participant(models.Model):
    name = models.CharField(max_length=10, null=False)
    email = models.EmailField(null=False)

class Category(models.Model):
    NOT_MENTIONED = "SELECT CATEGORY"
    SPORTS = "SPORTS"
    FESTIVAL = "FESTIVAL"
    SEMINAR = "SEMINAR"

    EVENT_CATEGORY = (
        (NOT_MENTIONED, "Select Category"),
        (SPORTS, "Sports"),
        (FESTIVAL, "Festival"),
        (SEMINAR, 'Seminar')
    )

    category_name = models.CharField(max_length=50, choices=EVENT_CATEGORY, null=False, default=NOT_MENTIONED)
    category_description = models.TextField()

class Event(models.Model):
    name = models.CharField(max_length=100, null=False)
    description = models.TextField(null=False)
    date = models.DateField(blank=False, null=False)
    time = models.CharField(max_length=50, blank=False, null=False)
    location = models.CharField(max_length=100, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category")
    participant = models.ManyToManyField(Participant, related_name="participant")


