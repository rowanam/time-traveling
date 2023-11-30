from . import views
from django.urls import path


urlpatterns = [
    path("", views.Welcome.as_view(), name="home"),
    path("dashboard/", views.TripList.as_view(), name="trips_dashboard"),
    path("add-trip/", views.AddTrip.as_view(), name="add_trip"),
]
