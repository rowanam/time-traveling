from django.test import TestCase


class TestWelcomeView(TestCase):
    def test_get_welcome_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "welcome.html")
