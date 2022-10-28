from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=250)
    author = models.CharField(max_length=250)
    description = models.TextField()
    price = models.PositiveIntegerField(default=0)
    publisher = models.CharField(max_length=250)
    translator = models.CharField(max_length=250, blank=True)
    cover = models.ImageField(upload_to='covers/')

    def __str__(self):
        return self.title
