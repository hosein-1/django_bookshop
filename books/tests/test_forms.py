from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model

from ..forms import CommentForm
from ..models import Book, Comment, Category
import datetime


class CommentFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        category1 = Category.objects.create(name='history', slug='history')
        book_test = Book.objects.create(
            title='test title 1',
            author='hosein',
            description='This is a test',
            price=2000,
            publisher='test_publisher',
            translator='parastoo',
            cover=SimpleUploadedFile('hosein.jpg', b"file_content", content_type='image/jpeg'),
            slug='test-title-1',
        )
        book_test.category.set([category1.pk])
        user = get_user_model().objects.create(email='ali@gmail.com')
        comment_test = Comment.objects.create(
            text='This is a comment for test.',
            author=user,
            book=book_test,
            datetime_created=datetime.datetime.now(),
        )
        cls.form1 = CommentForm(data={})
        cls.form2 = CommentForm(data={'text': 'This is comment2'})
        cls.form3 = CommentForm(data={'text': 'This is comment3',
                                      'parent': comment_test.id})

    def test_form_is_invalid(self):
        self.assertFalse(self.form1.is_valid())

    def test_form_is_valid(self):
        self.assertTrue(self.form2.is_valid())

    def test_form_is_valid_by_get_parent_field(self):
        self.assertTrue(self.form3.is_valid())
