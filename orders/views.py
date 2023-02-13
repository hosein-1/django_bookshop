from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from .forms import OrderForm
from .models import OrderItem


@login_required
def create_order(request):
    order_form = OrderForm()
    cart = Cart(request)

    if len(cart) == 0:
        redirect('books:book_list')

    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order_object = order_form.save(commit=False)
            order_object.user = request.user
            order_object.save()

            for item in cart:
                book = item['book_object']
                OrderItem.objects.create(
                    order=order_object,
                    book=book,
                    quantity=item['quantity'],
                    price=book.price
                )

            cart.clear()
            request.session['order_id'] = order_object.id
            return redirect('payment:payment_process')

    return render(request, 'orders/order_create.html', {'order_form': order_form})
