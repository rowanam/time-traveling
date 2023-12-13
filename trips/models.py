from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class CustomTrip(models.Model):
    """A class-based model for custom trips created by a user.
    A custom trip is one where the structure of the locations is not enforced -
    any type of location can be entered."""

    title = models.CharField(max_length=70)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_custom_trips"
    )
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    cover_image = CloudinaryField("image", blank=True, null=True)

    def __str__(self):
        """Return string representation of object"""
        return self.title


class CustomLocation(models.Model):
    """A class-based model for locations in a custom trip."""

    name = models.CharField(max_length=50)
    trip = models.ForeignKey(CustomTrip, on_delete=models.CASCADE, related_name="locations")
    lat = models.FloatField()
    long = models.FloatField()
    order = models.IntegerField()
