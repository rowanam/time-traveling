from django.shortcuts import render
from django.views import View


class TripList(View):
    def get(self, request):
        return render(request, "base.html")
