from django.db import models
from django.contrib.auth.models import User


class CustomTrip(models.Model):
    """A class-based model for custom trips created by a user.
    A custom trip is one where the structure of the locations is not enforced -
    any type of location can be entered."""

    title = models.CharField(max_length=70)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_custom_trips"
    )
    locations = models.JSONField()
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        """Return string representation of object"""
        return self.title
