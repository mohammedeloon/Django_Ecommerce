from django.shortcuts import render
from cart.cart import Cart
from payment.models import ShippingAddress
from store.models import Profile
from payment.forms import ShippingForm
from store.forms import UserInfoForm

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
        billing_user = Profile.objects.get(user__id=request.user.id)
        # Shipping Form
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        #shipping form
        UserInfo_Form = UserInfoForm(request.POST or None, instance=billing_user)
        return render(request, "payment/check_out.html", {"cart_products":cart_products, "cart_products_qty":cart_products_qty, "cart_total_price":cart_total_price, "shipping_form":shipping_form, 'billing_form':UserInfo_Form })
    else:
        # Checkout as guest
        shipping_form = ShippingForm(request.POST or None)
        UserInfo_Form = UserInfoForm(request.POST or None)
        return render(request, "payment/check_out.html", {"cart_products":cart_products, "cart_products_qty":cart_products_qty, "cart_total_price":cart_total_price, "shipping_form":shipping_form})
    