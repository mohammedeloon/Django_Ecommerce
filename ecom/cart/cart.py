from store.models import Product, Profile
class Cart():
    def __init__(self, request):
        self.session = request.session
        #get request
        self.request = request
        
        # get the current session key if existed
        cart = self.session.get('session_key')
        # this logic is necessary for the get_items fun, especially when the cart is empty. And if the user is new, create a session_key    
        if not cart or 'session_key' not in request.session:
            # If the cart doesn't exist, initialize it as an empty dictionary
            cart = self.session['session_key'] = {}
        # make the cart var available on all pages(global)
        self.cart = cart
       
    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)

        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = int(product_qty)
        self.session.modified = True

        # deal with logged in user 
        if self.request.user.is_authenticated:
            # get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # convert {'3': 1, '2': 3} to {"3": 1, "2": 3}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # save cart t0 profile model 
            current_user.update(old_cart=carty)

    def save_to_db(self):
            # deal with logged in user 
            if self.request.user.is_authenticated:
                # get the current user profile
                current_user = Profile.objects.filter(user__id=self.request.user.id)
                # convert {'3': 1, '2': 3} to {"3": 1, "2": 3}
                carty = str(self.cart)
                carty = carty.replace("\'", "\"")
                # save cart t0 profile model 
                current_user.update(old_cart=carty)    

    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)

        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = int(product_qty)
        self.session.modified = True

        self.save_to_db()
        
    def __len__(self):
        return len(self.cart)
    
    def get_items(self):
        products = []
        for product_id in self.cart.keys():
            products.append(Product.objects.get(id=product_id))
        return products
    
    def get_quantity(self):
        quantities = self.cart 
        return quantities
    
    def delete(self, product):
        product_id = str(product)
        if product_id in self.cart.keys():
            self.cart.pop(product_id)
        self.session.modified = True 

        self.save_to_db()


    def count_total(self):
        prices = []
        for product_id, qty in self.cart.items():
            product = Product.objects.get(id=product_id)
            if product.on_sale:
                product_price = product.sale_price * qty
                prices.append(product_price)
            else:
                product_price = product.price * qty
                prices.append(product_price)
        return sum(prices)
    
    def calculate_price(self, product, qty):
        product = Product.objects.get(id=product)
        price = 0
        if product.on_sale:
           price = product.sale_price * qty
        else:
           price = product.price * qty
        return price

   

            

        
		
        


