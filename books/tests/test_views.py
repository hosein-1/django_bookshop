from django.test import TestCase
from django.shortcuts import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model

from ..models import Book, Category, Comment
import datetime


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
    user = None

    @classmethod
    def setUpTestData(cls):
        category1 = Category.objects.create(name='novel', slug='novel')
        cls.user = get_user_model().objects.create(email='hosein@gmail.com')

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
        cls.comment1 = Comment.objects.create(
            text='This is a comment for test.',
            author=cls.user,
            book=cls.book2,
            datetime_created=datetime.datetime.now(),
        )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(f'/book/{self.book2.pk}/{self.book2.slug}/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('book_detail', kwargs={'pk': self.book2.pk, 'slug': self.book2.slug}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('book_detail', kwargs={'pk': self.book2.pk, 'slug': self.book2.slug}))
        self.assertTemplateUsed(response, 'books/book_detail.html')

    def test_view_404_status_if_book_id_not_exist(self):
        response = self.client.get('/book/2222/fff/')
        self.assertEqual(response.status_code, 404)

    def test_view_post_comment(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('book_detail', kwargs={'pk': self.book2.pk, 'slug': self.book2.slug}),
                                    {
                                        'text': 'The book is good',


                                    })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.last().text, 'The book is good')

    def test_view_post_comment_with_parent(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('book_detail', kwargs={'pk': self.book2.pk, 'slug': self.book2.slug}),
                                    {
                                        'text': 'The book is bad',
                                        'parent': self.comment1.id,
                                    })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.all()[1].text, 'The book is bad')
        self.assertEqual(Comment.objects.all()[1].parent, self.comment1)
