
class Cart():
    def __int__(self, request):
        self.request = request
        self.session = request.session

        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
            # cart = self.session['cart']

        self.cart = cart
