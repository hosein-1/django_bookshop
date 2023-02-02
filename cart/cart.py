from books.models import Book


class Cart:
    def __int__(self, request):
        self.request = request
        self.session = request.session

        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
            # cart = self.session['cart']

        self.cart = cart

    def add(self, book, quantity=1, replace_current_quantity=False):
        book_id = str(book.id)

        if book_id not in self.cart:
            self.cart[book_id] = {'quantity': quantity}

        if replace_current_quantity:
            self.cart[book_id]['quantity'] = quantity

        else:
            self.cart[book_id]['quantity'] += quantity

        self.save()

    def remove(self, book):
        book_id = str(book.id)

        if book_id in self.cart:
            del self.cart[book_id]
            self.save()

    def __iter__(self):
        book_ids = self.cart.keys()

        books = Book.objects.get(id__in=book_ids)
        cart = self.cart.copy()

        for book in books:
            cart[str(book.id)]['book_obj'] = book

        for item in cart.values():
            yield item

    def save(self):
        self.session.modified = True

