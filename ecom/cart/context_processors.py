from .cart import Cart 

#create a context processor so that our cart is available on all pages of the site
def cart(request):
    # Return the default data of our cart
    return {'cart': Cart(request)}