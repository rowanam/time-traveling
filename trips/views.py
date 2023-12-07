from django.shortcuts import render, reverse, get_object_or_404
from django.views import View
from django.http import HttpResponseRedirect
from django.forms import formset_factory
from .forms import CustomTripForm, CustomLocationsForm
from .models import CustomTrip, CustomLocation


class Welcome(View):
    """A class-based view for the welcome page - home page for non-logged-in users."""

    def get(self, request):
        return render(request, "welcome.html")


class TripList(View):
    """A class-based view for the trips dashboard page - home page for logged-in users."""

    def get(self, request):
        user = request.user
        trips = CustomTrip.objects.filter(user=user)
        context = {"trips": trips}
        return render(request, "trips_dashboard.html", context)


class TripDetail(View):
    """A class-based view to display details of a trip."""

    def get(self, request, trip_id):
        user = request.user
        user_trips_queryset = CustomTrip.objects.filter(user=user)
        trip = get_object_or_404(user_trips_queryset, id=trip_id)
        trip_locations = CustomLocation.objects.filter(trip=trip).order_by("order")

        coordinates_seq = [[location.lat, location.long] for location in trip_locations]

        context = {
            "trip": trip,
            "locations": trip_locations,
            "coordinates": coordinates_seq,
        }
        return render(request, "view_custom_trip.html", context)


class AddCustomTrip(View):
    """A class-based view for adding a new custom trip."""

    def get(self, request):
        """Render the add trip template"""
        form = CustomTripForm()
        context = {"form": form}
        return render(request, "add_custom_trip.html", context)

    def post(self, request):
        """Post the completed add trip form"""
        form = CustomTripForm(data=request.POST)

        if form.is_valid():
            new_trip = form.save(commit=False)
            new_trip.user = request.user
            new_trip.save()
            trip_id = new_trip.id
            return HttpResponseRedirect(reverse("add_custom_locations", args=[trip_id]))
        else:
            return render(request, "add_custom_trip.html", {"form": form})


class AddCustomLocations(View):
    """A class-based view for adding locations to a custom trip."""

    def get(self, request, trip_id):
        user = request.user
        user_trips_queryset = CustomTrip.objects.filter(user=user)
        trip = get_object_or_404(user_trips_queryset, id=trip_id)

        CustomLocationsFormSet = formset_factory(CustomLocationsForm, extra=0)
        formset = CustomLocationsFormSet()

        context = {"trip": trip, "formset": formset}

        return render(request, "add_custom_locations.html", context)

    def post(self, request, trip_id):
        user = request.user
        user_trips_queryset = CustomTrip.objects.filter(user=user)
        trip = get_object_or_404(user_trips_queryset, id=trip_id)

        CustomLocationsFormSet = formset_factory(CustomLocationsForm)
        formset = CustomLocationsFormSet(data=request.POST)
        if formset.is_valid():
            for form in formset:
                new_location = form.save(commit=False)
                new_location.trip = trip
                new_location.save()
        else:
            print("Error")

        return HttpResponseRedirect(reverse("trips_dashboard"))
