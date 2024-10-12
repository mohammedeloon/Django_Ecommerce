from store.models import Product
class Cart():
    def __init__(self, request):
        self.session = request.session
        
        # get the current session key if existed
        cart = self.session.get('session_key')
        # this logic is necessary for the get_items fun, especially when the cart is empty. And if the user is new, create a session_key    
        if not cart or 'session_key' not in request.session:
            # If the cart doesn't exist, initialize it as an empty dictionary
            cart = self.session['session_key'] = {}
        # make the cart var available on all pages(global)
        self.cart = cart
       
    def add(self, product):
        product_id = str(product.id)

        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = {'price': str(product.price)}
        self.session.modified = True

    def __len__(self):
        return len(self.cart)
    
    def get_items(self):
        products = []
        for product_id in self.cart.keys():
            products.append(Product.objects.get(id=product_id))
        return products
        
		
        


