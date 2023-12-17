from django.test import TestCase

# Get user model from settings
from django.contrib.auth import get_user_model

User = get_user_model()

from ..models import Trip, Location


class TestTripModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up test trip
        test_user = User.objects.create_user(username="testuser", password="Password*1")
        Trip.objects.create(title="Test Title", user=test_user)

    def test_title_max_length(self):
        trip = Trip.objects.get(id=1)
        max_length = trip._meta.get_field("title").max_length
        self.assertEqual(max_length, 70)

    def test_trip_string_method_returns_title(self):
        trip = Trip.objects.get(id=1)
        self.assertEqual(str(trip), "Test Title")


class TestLocationModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(username="testuser", password="Password*1")
        trip = Trip.objects.create(title="Test Title", user=test_user)
        Location.objects.create(name="Test", lat=0, long=0, order=1, trip=trip)

    def test_name_max_length(self):
        location = Location.objects.get(id=1)
        max_length = location._meta.get_field("name").max_length
        self.assertEqual(max_length, 50)

    def test_location_string_method_returns_name(self):
        location = Location.objects.get(id=1)
        self.assertEqual(str(location), "Test")
