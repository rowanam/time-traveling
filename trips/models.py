from django.db import models
from django.contrib.auth.models import User


class CustomTrip(models.Model):
    """ A class-based model for custom trips created by a user.
    A custom trip is one where the structure of the locations is not enforced -
    any type of location can be entered. """
    title = models.CharField(max_length=70)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_custom_trips")
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)


class CustomLocation(models.Model):
    """ A class-based model for the locations in a user-created custom trip. """
    trip = models.ForeignKey(CustomTrip, on_delete=models.CASCADE, related_name="locations")
    name = models.CharField(max_length=30, blank=True)
    g_place_id = models.CharField(max_length=200)
    order = models.IntegerField()
