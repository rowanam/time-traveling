from . import views
from django.urls import path


urlpatterns = [
    path("", views.Welcome.as_view(), name="home"),
    path("dashboard/", views.TripList.as_view(), name="trips_dashboard"),
    path("add-custom-trip/", views.AddCustomTrip.as_view(), name="add_custom_trip"),
    path("trip/<int:trip_id>", views.TripDetail.as_view(), name="view_custom_trip"),
    path("add-custom-locations/<int:trip_id>", views.AddCustomLocations.as_view(), name="add_custom_locations"),
]
