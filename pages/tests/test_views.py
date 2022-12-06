from django.test import TestCase
from django.shortcuts import reverse


class AboutUsViewTest(TestCase):
    def test_about_us_view_url_exists_at_desired_location(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)

    def test_about_us_view_url_accessible_by_name(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)

    def test_about_us_view_uses_correct_template(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/about_us.html')


class ContactUsViewTest(TestCase):
    def test_contact_us_view_url_exists_at_desired_location(self):
        response = self.client.get('/contactus/')
        self.assertEqual(response.status_code, 200)

    def test_contact_us_view_url_accessible_by_name(self):
        response = self.client.get(reverse('contact_us'))
        self.assertEqual(response.status_code, 200)

    def test_contact_us_view_uses_correct_template(self):
        response = self.client.get(reverse('contact_us'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/contact_us.html')