from books.models import Book


class Cart:
    """This class is made for cart system in this site."""
    def __int__(self, request):
        self.request = request
        self.session = request.session

        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
            # cart = self.session['cart']

        self.cart = cart

    def add(self, book, quantity=1, replace_current_quantity=False):
        """This function adds the  book to the cart.
        If the desired book does not exist in the shopping cart,
        it finds its ID from the database and stores its ID in the shopping cart."""
        book_id = str(book.id)

        if book_id not in self.cart:
            self.cart[book_id] = {'quantity': 0}

        if replace_current_quantity:
            self.cart[book_id]['quantity'] = quantity

        else:
            self.cart[book_id]['quantity'] += quantity

        self.save()

    def remove(self, book):
        """Removes the desired book from the shopping cart."""
        book_id = str(book.id)

        if book_id in self.cart:
            del self.cart[book_id]
            self.save()

    def __iter__(self):
        """This function returns all the values in the shopping cart."""
        book_ids = self.cart.keys()

        books = Book.objects.get(id__in=book_ids)
        cart = self.cart.copy()

        for book in books:
            cart[str(book.id)]['book_obj'] = book

        for item in cart.values():
            yield item

    def __len__(self):
        """Returns the number of items in the shopping cart."""
        return sum(item['quantity'] for item in self.cart.values())

    def clear(self):
        """Deletes all the items in the shopping cart."""
        del self.session['cart']
        self.save()

    def get_total_price(self):
        """It returns the sum of the total price of the shopping cart."""
        return sum(item['quantity'] * item['book_obj'] for item in self.cart.values())

    def save(self):
        self.session.modified = True

