from django.db import models
from django.urls import reverse


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
