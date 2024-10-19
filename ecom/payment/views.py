from django.shortcuts import render, redirect
from cart.cart import Cart
from payment.models import ShippingAddress
from store.models import Profile
from payment.forms import ShippingForm, PaymentForm
from store.forms import UserInfoForm
from django.contrib import messages

def payment_success(request):
    return render(request, 'payment/payment_success.html', {})

def check_out(request):
    cart = Cart(request)
    cart_products = cart.get_items()
    cart_products_qty = cart.get_quantity()
    cart_total_price = cart.count_total()
    if request.user.is_authenticated:
        # Checkout as logged in user
        # Shipping User
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        #billing user
        # billing_user = Profile.objects.get(user__id=request.user.id)
        # Shipping Form
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        #shipping form
        # UserInfo_Form = UserInfoForm(request.POST or None, instance=billing_user)
        return render(request, "payment/check_out.html", {"cart_products":cart_products, "cart_products_qty":cart_products_qty, "cart_total_price":cart_total_price, "shipping_form":shipping_form })
    else:
        # Checkout as guest
        shipping_form = ShippingForm(request.POST or None)
        return render(request, "payment/check_out.html", {"cart_products":cart_products, "cart_products_qty":cart_products_qty, "cart_total_price":cart_total_price, "shipping_form":shipping_form})
    
def billing_info(request):
    if request.POST: 
        cart = Cart(request)
        cart_products = cart.get_items()
        cart_products_qty = cart.get_quantity()
        cart_total_price = cart.count_total()
        if request.user.is_authenticated:
            # get the billing form 
            billing_form = PaymentForm()
            return render(request, "payment/billing_info.html", {"cart_products":cart_products, "cart_products_qty":cart_products_qty, "cart_total_price":cart_total_price, "shipping_info":request.POST, "billing_form": billing_form})
        else:
            billing_form = PaymentForm()
            return render(request, "payment/billing_info.html", {"cart_products":cart_products, "cart_products_qty":cart_products_qty, "cart_total_price":cart_total_price, "shipping_info":request.POST, "billing_form": billing_form})


    else:
        messages.error(request, 'Access Denied!')
        return redirect('index')