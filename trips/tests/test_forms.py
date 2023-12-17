from django.test import TestCase

# Get user model from settings
from django.contrib.auth import get_user_model
User = get_user_model()

from ..models import Trip
from ..forms import LocationInlineFormSet


# class TestLocationInlineFormSet(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         test_user = User.objects.create_user(username="testuser", password="Password*1")
#         Trip.objects.create(title="Test Trip", user=test_user)

#     def test_delete_field_is_hidden(self):
#         trip = Trip.objects.get(id=1)
#         formset = LocationInlineFormSet(instance=trip)
#         # for form in formset:
#         #     self.assertEqual(form.fields["DELETE"].widget, forms.HiddenInput())
