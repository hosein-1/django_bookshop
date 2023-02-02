
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

    def save(self):
        self.session.modified = True

