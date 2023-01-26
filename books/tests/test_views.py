from django.test import TestCase
from django.shortcuts import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from ..models import Book, Category


class BookListViewTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('book_list'))
        self.assertTemplateUsed(response, 'books/book_list.html')


class BookDetailViewTest(TestCase):
    book2 = None

    @classmethod
    def setUpTestData(cls):
        category1 = Category.objects.create(name='novel', slug='novel')

        cls.book2 = Book.objects.create(
            title='test title2',
            author='ali',
            description='This is a test',
            price=4000,
            publisher='test_publisher',
            translator='saeed',
            cover=SimpleUploadedFile('file.jpg', b"file_content", content_type='image/jpeg'),
            slug='test-title-2',

        )
        cls.book2.category.set([category1.pk])

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(f'/book/{self.book2.pk}/{self.book2.slug}/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('book_detail', kwargs={'pk': self.book2.pk, 'slug': self.book2.slug}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('book_detail', kwargs={'pk': self.book2.pk, 'slug': self.book2.slug}))
        self.assertTemplateUsed(response, 'books/book_detail.html')
