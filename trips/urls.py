from . import views
from django.urls import path


urlpatterns = [
    path("", views.Welcome.as_view(), name="home"),
    path("dashboard/", views.TripList.as_view(), name="trips_dashboard"),
    path("add-trip/", views.AddTrip.as_view(), name="add_trip"),
    path("trip/<int:trip_id>", views.TripDetail.as_view(), name="view_trip"),
    path("add-locations/<int:trip_id>", views.AddLocations.as_view(), name="add_locations"),
    path("locations/<int:pk>", views.UpdateLocations.as_view(), name="locations"),
    path("delete-trip/<int:trip_id>", views.DeleteTrip.as_view(), name="delete_trip"),
]
