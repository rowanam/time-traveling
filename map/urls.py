from . import views
from django.urls import path


urlpatterns = [
    path("map/", views.Map.as_view(), name="map"),
]
