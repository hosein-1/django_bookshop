from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.shortcuts import reverse

from ..models import Book, Category, Comment
import datetime


class BookModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category1 = Category.objects.create(name='novel', slug='novel')
        cls.book1 = Book.objects.create(
            title='test title 1',
            author='hosein',
            description='This is a test',
            price=2000,
            publisher='test_publisher',
            translator='parastoo',
            cover=SimpleUploadedFile('file.jpg', b"file_content", content_type='image/jpeg'),
            slug='test-title-1',
        )
        cls.book1.category.set([cls.category1.pk])

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
        cls.book2.category.set([cls.category1.pk])

    def test_book_model_str(self):
        expected_object_name = f'{self.book2.title} : {self.book2.author}'
        self.assertEqual(str(self.book2), expected_object_name)

    def test_book_model_slug_field_create_by_title(self):
        self.assertEqual(self.book1.slug, 'test-title-1')

    def test_book_model_get_absolute_url(self):
        book = Book.objects.get(id=1)
        self.assertEqual(book.get_absolute_url(), '/book/1/test-title-1/')

