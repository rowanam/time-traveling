from django.shortcuts import render
from django.views import View


class Welcome(View):
    def get(self, request):
        return render(request, "welcome.html")


class TripList(View):
    def get(self, request):
        return render(request, "trips-dashboard.html")
