from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from .cart import Cart
from books.models import Book
from .forms import AddToCartBookForm


def cart_detail_view(request):
    cart = Cart(request)
    for item in cart:
        item['book_update_quantity'] = AddToCartBookForm(initial={
            'quantity': item['quantity'],
            'inplace': True,
        })
    return render(request, 'cart/cart_detail.html', {'cart': cart})


@require_POST
def add_to_cart_view(request, book_id):
    cart = Cart(request)
    book = get_object_or_404(Book, id=book_id)
    form = AddToCartBookForm(request.POST)

    if form.is_valid():
        cleaned_data = form.cleaned_data
        quantity = cleaned_data['quantity']
        cart.add(book, quantity, replace_current_quantity=cleaned_data['inplace'])
    return redirect('cart:cart_detail')


def remove_specific_book_from_cart(request, book_id):
    cart = Cart(request)
    book = get_object_or_404(Book, id=book_id)
    cart.remove(book)
    return redirect('cart:cart_detail')


@require_POST
def clear_cart(request):
    cart = Cart(request)

    if len(cart):
        cart.clear()
    else:
        return redirect('books:book_list')

    return redirect('books:book_list')
