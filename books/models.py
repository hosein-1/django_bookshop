from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, unique=True, allow_unicode=True)


class Book(models.Model):
    title = models.CharField(max_length=250)
    author = models.CharField(max_length=250)
    description = models.TextField()
    price = models.PositiveIntegerField(default=0)
    publisher = models.CharField(max_length=250)
    translator = models.CharField(max_length=250, blank=True)
    cover = models.ImageField(upload_to='covers/')
    slug = models.SlugField(max_length=100, allow_unicode=True)
    category = models.ManyToManyField(Category)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book_detail', kwargs={'slug': self.slug, 'pk': self.id})


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comments')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')
    datetime_created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    @property
    def children(self):
        return Comment.objects.filter(parent=self).reverse()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False

    def get_absolute_url(self):
        return reverse('book_detail', kwargs={'slug': self.book.slug, 'pk': self.book.id})
