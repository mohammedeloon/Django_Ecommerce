class Cart():
    def __init__(self, request):
        self.session = request.session
        
        # get the current session key if existed
        cart = self.session.get('session_key')
        # make the cart var available on all pages(global)
        self.cart = cart

        # if the user is new, create a session_key
        if 'session_key' not in cart:
            cart = self.session['session_key'] = {} 

    def add(self, product):
        product_id = str(product.id)

        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = {'price': str(product.price)}
        self.session.modified = True


