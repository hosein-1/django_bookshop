from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(_('Name'), max_length=200)
    slug = models.SlugField(_('Slug'), max_length=100, unique=True, allow_unicode=True)


class Book(models.Model):
    title = models.CharField(_('Title'), max_length=250)
    author = models.CharField(_('Author'), max_length=250)
    description = models.TextField(_('Description'))
    price = models.PositiveIntegerField(_('Price'), default=0)
    publisher = models.CharField(_('Publisher'), max_length=250)
    translator = models.CharField(_('Translator'), max_length=250, blank=True)
    cover = models.ImageField(_('Cover'), upload_to='covers/')
    slug = models.SlugField(_('Slug'), max_length=100, allow_unicode=True)
    category = models.ManyToManyField(Category, verbose_name=_('Category'))

    def __str__(self):
        return f'{self.title} : {self.author}'

    def get_absolute_url(self):
        return reverse('books:book_detail', kwargs={'slug': self.slug, 'pk': self.id})


class Comment(models.Model):
    text = models.TextField(_('Text'), )
    author = models.ForeignKey(get_user_model(),
                               on_delete=models.CASCADE,
                               related_name='comments',
                               verbose_name=_('Author'))
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments', verbose_name=_('Book'))
    datetime_created = models.DateTimeField(_('Datetime_Created'), auto_now_add=True)
    active = models.BooleanField(_('Active'), default=True)
    parent = models.ForeignKey('self',
                               null=True,
                               blank=True,
                               on_delete=models.CASCADE,
                               related_name='replies',
                               verbose_name='Parent')

    @property
    def children(self):
        return Comment.objects.filter(parent=self).reverse()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False

    def __str__(self):
        return f'{self.author}'

    def get_absolute_url(self):
        return reverse('book_detail', kwargs={'slug': self.book.slug, 'pk': self.book.id})
