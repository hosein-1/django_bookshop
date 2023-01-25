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


class CommentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category1 = Category.objects.create(name='novel', slug='novel')
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

        cls.user = get_user_model().objects.create(email='hosein@gmail.com')
        cls.comment1 = Comment.objects.create(
            text='This is a comment for test.',
            author=cls.user,
            book=cls.book2,
            datetime_created=datetime.datetime.now(),
        )
        cls.comment2 = Comment.objects.create(
            text='This is a comment for test1.',
            author=cls.user,
            book=cls.book2,
            datetime_created=datetime.datetime.now(),
            active=False,
            parent=cls.comment1,

        )

    def test_comment_text(self):
        self.assertEqual(self.comment1.text, 'This is a comment for test.')

    def test_comment_is_parent_or_not(self):
        self.assertEqual(self.comment1.parent, None)
        self.assertEqual(self.comment2.parent, self.comment1)

    def test_active_comment_show_in_book_detail(self):
        response = self.client.get(reverse('book_detail', kwargs={'pk': self.book2.pk, 'slug': self.book2.slug}))
        self.assertEqual(self.comment1.active, True)
        self.assertContains(response, self.comment1.text)

    def test_inactive_comment_not_show_in_book_detail(self):
        response = self.client.get(reverse('book_detail', kwargs={'pk': self.book2.pk, 'slug': self.book2.slug}))
        self.assertEqual(self.comment2.active, False)
        self.assertNotContains(response, self.comment2.text)