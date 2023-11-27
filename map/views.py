from django.shortcuts import render
from django.views import View
import os


class Map(View):
    def get(self, request):
        maps_api_key = os.environ.get("GOOGLE_MAPS_API_KEY")
        return render(
            request,
            "map.html",
            {"maps_api_key": maps_api_key},
        )
