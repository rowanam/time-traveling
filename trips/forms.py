from django import forms
from django.utils.translation import gettext_lazy as _
from .models import CustomTrip, CustomLocation


class CustomTripForm(forms.ModelForm):
    """A form for creating new custom trips."""

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
        model = CustomTrip
        fields = ["title", "start_date", "end_date", "note", "cover_image"]
        labels = {
            "title": _("Title*"),
        }


class CustomLocationsForm(forms.ModelForm):
    """A form for adding locations to custom trips."""

    lat = forms.DecimalField(widget=forms.HiddenInput())
    long = forms.DecimalField(widget=forms.HiddenInput())
    order = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = CustomLocation
        fields = ["name", "lat", "long", "order"]
        labels = {
            "name": _("Location name"),
        }
