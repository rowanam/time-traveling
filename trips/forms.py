from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Trip, Location


class TripForm(forms.ModelForm):
    """A form for creating a new trip."""

    start_date = forms.DateField(
        widget=forms.DateInput(format="%b %-d, %Y", attrs={"class": "datepicker"}),
        input_formats=("%b %-d, %Y", "%b %d, %Y"),
        required=False,
    )
    end_date = forms.DateField(
        widget=forms.DateInput(format="%b %-d, %Y", attrs={"class": "datepicker"}),
        input_formats=("%b %-d, %Y", "%b %d, %Y"),
        required=False,
    )

    class Meta:
        model = Trip
        fields = ["title", "start_date", "end_date", "note", "cover_image"]
        labels = {
            "title": _("Title*"),
        }


class LocationForm(forms.ModelForm):
    """A form for creating a new location in a trip."""

    lat = forms.DecimalField(widget=forms.HiddenInput())
    long = forms.DecimalField(widget=forms.HiddenInput())
    order = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = Location
        fields = ["name", "lat", "long", "order"]
        labels = {
            "name": _("Location name"),
        }
