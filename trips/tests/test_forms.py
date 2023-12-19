from django.test import TestCase
from datetime import datetime
from ..forms import TripForm


class TestTripForm(TestCase):
    def test_start_date_requires_end_date(self):
        start_date_object = datetime.strptime("Nov 13, 2023", "%b %d, %Y")
        form = TripForm({"title": "Test", "start_date": start_date_object})
        self.assertFalse(form.is_valid())
        self.assertIn("end_date", form.errors.keys())

    def test_end_date_requires_start_date(self):
        end_date_object = datetime.strptime("Dec 13, 2023", "%b %d, %Y")
        form = TripForm({"title": "Test", "end_date": end_date_object})
        self.assertFalse(form.is_valid())
        self.assertIn("start_date", form.errors.keys())

    def test_end_date_must_be_after_start_date(self):
        start_date_object = datetime.strptime("Dec 13, 2023", "%b %d, %Y")
        end_date_object = datetime.strptime("Nov 13, 2023", "%b %d, %Y")
        form = TripForm(
            {
                "title": "Test",
                "start_date": start_date_object,
                "end_date": end_date_object,
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("end_date", form.errors.keys())
