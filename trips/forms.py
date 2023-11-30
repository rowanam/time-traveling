from django import forms
from .models import CustomTrip


class CustomTripForm(forms.ModelForm):
    """ A form for creating new custom trips. """
    class Meta:
        model = CustomTrip
        fields = ["title", "start_date", "end_date"]
