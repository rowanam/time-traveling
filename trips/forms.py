from django import forms
from .models import CustomTrip, CustomLocation


class CustomTripForm(forms.ModelForm):
    """ A form for creating new custom trips. """
    class Meta:
        model = CustomTrip
        fields = ["title", "start_date", "end_date"]


class CustomLocationForm(forms.ModelForm):
    """ A form for adding a location to a custom trip. """
    class Meta:
        model = CustomLocation
        fields = ["name", "g_place_id", "order"]
