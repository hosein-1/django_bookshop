from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from phonenumber_field.modelfields import PhoneNumberField

from books.models import Book


class Order(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name=_('User'))
    first_name = models.CharField(_('First_name'), max_length=100)
    last_name = models.CharField(_('Last_name'), max_length=100)
    phone_number = PhoneNumberField(_('Phone_Number'))
    address = models.CharField(_('Address'), max_length=800)
    order_notes = models.CharField(_('Notes'), max_length=800)
    is_paid = models.BooleanField(default=False)
    datetime_created = models.DateTimeField(auto_now=True)
    datetime_modified = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order {self.id} : {self.first_name} {self.last_name} {self.is_paid}'

    def get_total_price(self):
        return sum(item.price * item.quantity for item in self.order_items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items', verbose_name=_('Order'))
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name=_('Book'))
    quantity = models.PositiveIntegerField(_('Quantity'), default=1)
    price = models.PositiveIntegerField(_('Price'))

    def __str__(self):
        return f'{self.order} -> {self.book.title}'