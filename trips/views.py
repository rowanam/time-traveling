from django.shortcuts import render, reverse, get_object_or_404
from django.views import View
from django.http import HttpResponseRedirect
from .forms import CustomTripForm
from .models import CustomTrip


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

        # sample coordinates
        coordinates = [[45.51, -122.68], [37.77, -122.43], [34.04, -118.2]]

        context = {
            "trip": trip,
            "coordinates": coordinates,
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
        else:
            print("Error")

        return HttpResponseRedirect(reverse("trips_dashboard"))
