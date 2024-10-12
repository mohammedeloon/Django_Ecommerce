from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from .cart import Cart
from django.http import JsonResponse


def cart_summary(request):
    cart = Cart(request)
    products = cart.get_items()
    return render(request, 'cart_summary.html', {'cart': products})

def add_cart(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post': 
         # get data
         product_id = int(request.POST.get('product_id'))
         # look up product in the database
         product = get_object_or_404(Product, id=product_id)
         #save_to_session
         cart.add(product=product)
         # get cart quantity
         cart_quantity =cart.__len__()
         # return response
         response = JsonResponse({'cart_quantity: ': cart_quantity})
         return response

def update_cart(request):
    pass

def delete_cart(request):
    pass