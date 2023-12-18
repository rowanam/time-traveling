from . import views
from django.urls import path


urlpatterns = [
    path("", views.Welcome.as_view(), name="home"),
    path("dashboard/", views.TripList.as_view(), name="trips_dashboard"),
    path("add-trip/", views.AddTrip.as_view(), name="add_trip"),
    path("trip/<int:trip_id>", views.TripDetail.as_view(), name="view_trip"),
    path("edit-trip/<int:pk>", views.EditTrip.as_view(), name="edit_trip"),
    path("delete-trip/<int:trip_id>", views.DeleteTrip.as_view(), name="delete_trip"),
    path("locations/<int:pk>", views.UpdateLocations.as_view(), name="locations"),
    path("life-map/", views.LifeMap.as_view(), name="life_map"),
]
