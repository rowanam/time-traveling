from django.test import TestCase

# Get user model from settings
from django.contrib.auth import get_user_model

User = get_user_model()

from ..models import Trip, Location


class TestWelcomeView(TestCase):
    def test_get_welcome_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "welcome.html")


class TestTripListView(TestCase):
    @classmethod
    def setUpTestData(self):
        test_user1 = User.objects.create_user(
            username="testuser1", password="Password*1"
        )
        test_user2 = User.objects.create_user(
            username="testuser2", password="Password*1"
        )

        # create 3 and 5 test trips for each user, respectively
        for _ in range(3):
            Trip.objects.create(title="Test Title", user=test_user1)

        for _ in range(5):
            Trip.objects.create(title="Test Title", user=test_user2)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get("/dashboard/")
        self.assertRedirects(response, "/accounts/login/?next=/dashboard/")

    def test_get_dashboard_page_if_logged_in(self):
        # log a test user in
        self.client.login(username="testuser1", password="Password*1")
        response = self.client.get("/dashboard/")

        # check user is logged in
        self.assertEqual(str(response.context["user"]), "testuser1")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "trips_dashboard.html")

    def test_only_display_user_trips(self):
        self.client.login(username="testuser1", password="Password*1")
        response = self.client.get("/dashboard/")

        # check there are 3 trips in context
        self.assertTrue("trips" in response.context)
        self.assertEqual(len(response.context["trips"]), 3)

        # check the trips belong to testuser1 and have ids 1-3
        for trip, trip_id in zip(response.context["trips"], range(1, 3)):
            self.assertEqual(trip.user, response.context["user"])
            self.assertEqual(trip.id, trip_id)


class TestTripDetailView(TestCase):
    @classmethod
    def setUpTestData(self):
        test_user1 = User.objects.create_user(
            username="testuser1", password="Password*1"
        )
        test_user2 = User.objects.create_user(
            username="testuser2", password="Password*1"
        )

        # create a trip
        trip = Trip.objects.create(title="Test Title", user=test_user1)

        # create 3 locations in trip
        for _ in range(3):
            Location.objects.create(name="Test", lat=0, long=0, order=1, trip=trip)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get("/trip/1")
        self.assertRedirects(response, "/accounts/login/?next=/trip/1")

    def test_404_response_if_trip_not_belong_to_logged_in_user(self):
        # log in testuser2
        self.client.login(username="testuser2", password="Password*1")
        response = self.client.get("/trip/1")

        # check for 404 response
        self.assertEqual(response.status_code, 404)

    def test_get_trip_detail_page_if_correct_logged_in_user(self):
        # log in testuser1
        self.client.login(username="testuser1", password="Password*1")
        response = self.client.get("/trip/1")

        # check user is logged in
        self.assertEqual(str(response.context["user"]), "testuser1")

        # check success status code and correct template
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "view_trip.html")

        # check trip, locations and locations coordinates are in context
        self.assertTrue("trip" in response.context)
        self.assertTrue("locations" in response.context)
        self.assertTrue("coordinates" in response.context)

        # check trip belongs to logged in user
        trip = Trip.objects.get(id=1)
        self.assertEqual(trip.user, response.context["user"])

        # check context contains 3 locations
        self.assertEqual(len(response.context["locations"]), 3)
