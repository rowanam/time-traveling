from django.shortcuts import render, reverse
from django.views import View
from django.http import HttpResponseRedirect
from .forms import CustomTripForm


class Welcome(View):
    """A class-based view for the welcome page - home page for non-logged-in users."""

    def get(self, request):
        return render(request, "welcome.html")


class TripList(View):
    """A class-based view for the trips dashboard page - home page for logged-in users."""

    def get(self, request):
        return render(request, "trips_dashboard.html")


class AddTrip(View):
    """A class-based view for adding a new trip."""

    def get(self, request):
        """ Render the add trip template """
        form = CustomTripForm()
        context = {"form": form}
        return render(request, "add_trip.html", context)

    def post(self, request):
        """ Post the completed add trip form """
        form = CustomTripForm(data=request.POST)

        if form.is_valid():
            new_trip = form.save(commit=False)
            new_trip.user = request.user
            new_trip.save()
        else:
            print("Error")

        return HttpResponseRedirect(reverse("trips_dashboard"))
