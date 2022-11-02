from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Book


class BookListPageTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.book1 = Book.objects.create(
            title='book1',
            author='hosein',
            description='This is a text',
            price=2000,
            publisher='shaparak',
            cover=SimpleUploadedFile('file.jpg', b"file_content", content_type='image/jpeg')

        )

    def test_book_list_page_url(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_book_list_page_url_by_name(self):
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 200)

    def test_book_list_page_template_used(self):
        response = self.client.get(reverse('book_list'))
        self.assertTemplateUsed(response, 'books/books_list.html')

    def test_book_list_page_show_book_title(self):
        response = self.client.get((reverse('book_list')))
        self.assertContains(response, self.book1.title)

    def test_book_list_page_show_book_image(self):
        response = self.client.get(reverse('book_list'))
        self.assertContains(response, self.book1.cover)


