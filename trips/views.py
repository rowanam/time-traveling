from django.shortcuts import render, reverse, get_object_or_404
from django.views import View
from django.views.generic.edit import CreateView, UpdateView
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import F
from extra_views import InlineFormSetView, FormSetSuccessMessageMixin
from .forms import TripForm, LocationForm, LocationInlineFormSet
from .models import Trip, Location


class Welcome(View):
    """A class-based view for the welcome page - home page for non-logged-in users."""

    def get(self, request):
        return render(request, "welcome.html")


class TripList(LoginRequiredMixin, View):
    """A class-based view for the trips dashboard page - home page for logged-in users."""

    def get(self, request):
        user = request.user
        trips = Trip.objects.filter(user=user).order_by(
            F("start_date").desc(nulls_last=True)
        )
        context = {"trips": trips}
        return render(request, "trips_dashboard.html", context)


class TripDetail(LoginRequiredMixin, View):
    """A class-based view to display details of a trip."""

    def get(self, request, trip_id):
        user = request.user
        user_trips_queryset = Trip.objects.filter(user=user)
        trip = get_object_or_404(user_trips_queryset, id=trip_id)
        trip_locations = Location.objects.filter(trip=trip).order_by("order")

        coordinates_seq = [[location.lat, location.long] for location in trip_locations]

        context = {
            "trip": trip,
            "locations": trip_locations,
            "coordinates": coordinates_seq,
        }
        return render(request, "view_trip.html", context)


class AddTrip(LoginRequiredMixin, CreateView):
    """A class-based view for creating a trip."""

    model = Trip
    form_class = TripForm
    template_name = "add_trip.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        messages.success(self.request, f"{self.object.title} created successfully.")
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("locations", args=[self.object.pk])


class EditTrip(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """A class-based view for updating a trip."""

    model = Trip
    form_class = TripForm
    template_name = "edit_trip.html"
    success_message = "%(title)s updated successfully."

    def get_queryset(self):
        return Trip.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse("locations", args=[self.object.pk])


class DeleteTrip(LoginRequiredMixin, View):
    """A class-based view for deleting a trip."""

    def get(self, request, trip_id):
        user = request.user
        user_trips_queryset = Trip.objects.filter(user=user)
        trip = get_object_or_404(user_trips_queryset, id=trip_id)
        trip.delete()
        messages.success(request, f"{trip.title} deleted successfully.")
        return HttpResponseRedirect(reverse("trips_dashboard"))


class UpdateLocations(
    LoginRequiredMixin, FormSetSuccessMessageMixin, InlineFormSetView
):
    """A class-based view for changing location records associated with a trip."""

    model = Trip
    inline_model = Location
    form_class = LocationForm
    formset_class = LocationInlineFormSet
    factory_kwargs = {"extra": 0}
    template_name = "update_locations.html"
    success_message = "Locations saved successfully."

    def get_queryset(self):
        return Trip.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        """Pass context data to the view. Used here to pass initial location cordinates."""
        context = super().get_context_data(**kwargs)
        trip_locations = Location.objects.filter(trip=self.object).order_by("order")
        coordinates_seq = [[loc.lat, loc.long] for loc in trip_locations]
        context["coordinates"] = coordinates_seq
        return context

    def get_success_url(self):
        return reverse("view_trip", args=[self.object.pk])


class LifeMap(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        trips = Trip.objects.filter(user=user)

        coordinates = []

        # get a list of coordinates pairs for each trip
        for trip in trips:
            locations = Location.objects.filter(trip=trip).order_by("order")
            coordinates.append([[l.lat, l.long] for l in locations])

        context = {"coordinates": coordinates}

        return render(request, "life_map.html", context)
