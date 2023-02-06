from django.shortcuts import render, get_object_or_404, redirect

from .cart import Cart
from books.models import Book
from .forms import AddToCartBookForm


def cart_detail_view(request):
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})


def add_to_cart_view(request, book_id):
    cart = Cart(request)
    book = get_object_or_404(Book, id=book_id)
    form = AddToCartBookForm(request.POST)

    if form.is_valid():
        cleaned_data = form.cleaned_data
        quantity = cleaned_data['quantity']
        cart.add(book, quantity)
    return redirect('cart:cart_detail')
