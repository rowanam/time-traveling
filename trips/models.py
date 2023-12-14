from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class Trip(models.Model):
    """A class-based model for a trip created by a user."""

    title = models.CharField(max_length=70)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_trips"
    )
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    cover_image = CloudinaryField("image", blank=True, null=True)

    def __str__(self):
        """Return string representation of object"""
        return f"{self.title}"


class Location(models.Model):
    """A class-based model for a location in a trip."""

    name = models.CharField(max_length=50)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="locations")
    lat = models.FloatField()
    long = models.FloatField()
    order = models.IntegerField()

    def __str__(self):
        """Return string representation of object"""
        return f"{self.name}"
