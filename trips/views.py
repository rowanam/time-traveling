from django.shortcuts import render
from django.views import View


class Welcome(View):
    """ A class-based view for the welcome page - home page for non-logged-in users. """
    def get(self, request):
        return render(request, "welcome.html")


class TripList(View):
    """ A class-based view for the trips dashboard page - home page for logged-in users. """
    def get(self, request):
        return render(request, "trips_dashboard.html")


class AddTrip(View):
    """ A class-based view for adding a new trip. """
    def get(self, request):
        return render(request, "add_trip.html")
