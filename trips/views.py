from django.shortcuts import render, reverse, get_object_or_404
from django.views import View
from django.http import HttpResponseRedirect
from django.forms import formset_factory
from .forms import CustomTripForm, CustomLocationForm
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
        context = {
            "trips": trips
        }
        return render(request, "trips_dashboard.html", context)


class AddCustomTrip(View):
    """A class-based view for adding a new custom trip."""

    def get(self, request):
        """ Render the add trip template """
        form = CustomTripForm()
        context = {"form": form}
        return render(request, "add_custom_trip.html", context)

    def post(self, request):
        """ Post the completed add trip form """
        form = CustomTripForm(data=request.POST)

        if form.is_valid():
            new_trip = form.save(commit=False)
            new_trip.user = request.user
            new_trip.save()
            trip_pk = new_trip.id
        else:
            print("Error")

        return HttpResponseRedirect(reverse("add_custom_locations", args=[trip_pk]))


class AddCustomLocations(View):
    """A class-based view for adding locations to a custom trip."""

    def get(self, request, trip_pk):
        user = request.user
        user_trips_queryset = CustomTrip.objects.filter(user=user)
        trip = get_object_or_404(user_trips_queryset, id=trip_pk)

        CustomLocationsFormSet = formset_factory(CustomLocationForm)
        formset = CustomLocationsFormSet()

        # form = CustomLocationForm()
        context = {"trip": trip, "formset": formset}
        return render(request, "add_custom_locations.html", context)

    def post(self, request, trip_pk):
        user = request.user
        user_trips_queryset = CustomTrip.objects.filter(user=user)
        trip = get_object_or_404(user_trips_queryset, id=trip_pk)

        CustomLocationsFormSet = formset_factory(CustomLocationForm)
        formset = CustomLocationsFormSet(request.POST, request.FILES)

        print(formset)

        if formset.is_valid():
            for form in formset:
                new_location = form.save(commit=False)
                new_location.trip = trip
                new_location.save()
        else:
            print("Error")

        return HttpResponseRedirect(reverse("trips_dashboard"))
