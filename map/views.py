from django.shortcuts import render
from django.views import View


class Map(View):
    def get(self, request):
        return render(
            request,
            "map.html"
        )
