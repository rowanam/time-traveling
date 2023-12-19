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
        widgets = {
            "note": forms.Textarea(attrs={"rows": 4}),
        }

    def clean(self):
        start_date = self.cleaned_data.get("start_date")
        end_date = self.cleaned_data.get("end_date")

        if start_date and not end_date:
            msg = forms.ValidationError("End date is required if start date supplied.")
            self.add_error("end_date", msg)
        elif not start_date and end_date:
            msg = forms.ValidationError("Start date is required if end date supplied.")
            self.add_error("start_date", msg)
        elif start_date and end_date:
            if end_date < start_date:
                msg = forms.ValidationError("End date must be after start date.")
                self.add_error("end_date", msg)


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
        ordering = ("order",)
        widgets = {
            "name": forms.TextInput(attrs={"required": True}),
        }


class LocationInlineFormSet(forms.models.BaseInlineFormSet):
    """Override the BaseInlineFormSet class to hide "delete" field in the location formset."""

    def add_fields(self, form, index):
        super().add_fields(form, index)
        if "DELETE" in form.fields:
            form.fields["DELETE"].widget = forms.HiddenInput()
