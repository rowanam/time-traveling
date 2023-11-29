from . import views
from django.urls import path


urlpatterns = [
    path("dashboard/", views.TripList.as_view(), name="trips_dashboard"),
    path("", views.Welcome.as_view(), name="home")
]
