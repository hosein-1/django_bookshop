from django.test import TestCase
from django.urls import reverse


class HomePageTests(TestCase):
    def test_home_page_url(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home_page_url_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_page_template_used(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'pages/home.html')


class AboutUsPageTests(TestCase):
    def test_about_us_page_url(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)

    def test_about_us_page_url_by_name(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)

    def test_about_us_page_template_used(self):
        response = self.client.get(reverse('about'))
        self.assertTemplateUsed(response, 'pages/about_us.html')
