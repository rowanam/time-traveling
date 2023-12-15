from django.shortcuts import render, reverse, get_object_or_404
from django.views import View
from django.views.generic.edit import UpdateView
from django.http import HttpResponseRedirect
from django.forms import formset_factory
from extra_views import InlineFormSetView
from .forms import TripForm, LocationForm
from .models import Trip, Location


class Welcome(View):
    """A class-based view for the welcome page - home page for non-logged-in users."""

    def get(self, request):
        return render(request, "welcome.html")


class TripList(View):
    """A class-based view for the trips dashboard page - home page for logged-in users."""

    def get(self, request):
        user = request.user
        trips = Trip.objects.filter(user=user)
        context = {"trips": trips}
        return render(request, "trips_dashboard.html", context)


class TripDetail(View):
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


class AddTrip(View):
    """A class-based view for adding a new trip."""

    def get(self, request):
        """Render the add trip template"""
        form = TripForm()
        context = {"form": form}
        return render(request, "add_trip.html", context)

    def post(self, request):
        """Post the completed add trip form"""
        form = TripForm(data=request.POST)

        if form.is_valid():
            new_trip = form.save(commit=False)
            new_trip.user = request.user
            new_trip.save()
            trip_id = new_trip.id
            return HttpResponseRedirect(reverse("locations", args=[trip_id]))
        else:
            return render(request, "add_trip.html", {"form": form})


class EditTrip(UpdateView):
    """A class-based view for updating a trip."""

    model = Trip
    form_class = TripForm
    template_name = "edit_trip.html"

    def get_success_url(self):
        return reverse("locations", args=[self.object.pk])


class AddLocations(View):
    """A class-based view for adding locations to a trip."""

    def get(self, request, trip_id):
        user = request.user
        user_trips_queryset = Trip.objects.filter(user=user)
        trip = get_object_or_404(user_trips_queryset, id=trip_id)

        LocationsFormSet = formset_factory(LocationForm, extra=0)
        formset = LocationsFormSet()

        context = {"trip": trip, "formset": formset}

        return render(request, "add_locations.html", context)

    def post(self, request, trip_id):
        user = request.user
        user_trips_queryset = Trip.objects.filter(user=user)
        trip = get_object_or_404(user_trips_queryset, id=trip_id)

        LocationsFormSet = formset_factory(LocationForm)
        formset = LocationsFormSet(data=request.POST)

        if formset.is_valid():
            for form in formset:
                new_location = form.save(commit=False)
                new_location.trip = trip
                new_location.save()
            return HttpResponseRedirect(reverse("trips_dashboard"))
        else:
            print("Error")
            context = {"trip": trip, "formset": formset}
            return render(request, "add_locations.html", context)


class UpdateLocations(InlineFormSetView):
    model = Trip
    inline_model = Location
    form_class = LocationForm
    factory_kwargs = {"extra": 0}
    template_name = "update_locations.html"


class DeleteTrip(View):
    """A class-based view for deleting a trip."""

    def get(self, request, trip_id):
        user = request.user
        user_trips_queryset = Trip.objects.filter(user=user)
        trip = get_object_or_404(user_trips_queryset, id=trip_id)
        trip.delete()
        return HttpResponseRedirect(reverse("trips_dashboard"))
