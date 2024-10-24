import datetime
from django.shortcuts import render, redirect
from cart.cart import Cart
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User
from store.models import Profile, Product
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

        #create a session with shipping info 
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping
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
    
def process_order(request):
    if request.POST:
        # gather cart info
        cart = Cart(request)
        cart_products = cart.get_items()
        cart_products_qty = cart.get_quantity()
        cart_total_price = cart.count_total()
        
        # Get Billing Info From the Last Page
        payment_Form = PaymentForm(request.POST or None)
        # Get Shipping Session Data created in the billing info view
        my_shipping = request.session.get('my_shipping')
        #gather user info
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        my_address = "{0}\n{1}\n{2}\n{3}\n{4}\n{5}\n".format(
            my_shipping['shipping_address1'],
            my_shipping['shipping_address2'],
            my_shipping['shipping_city'],
            my_shipping['shipping_state'],
            my_shipping['shipping_zipcode'],
            my_shipping['shipping_country']
        )
        amount_paid = cart_total_price

        if request.user.is_authenticated:
            # logged in
            user = request.user
            # create order for logged in users
            order = Order(user=user, full_name=full_name, email=email, ShippingAddress=my_address, amount_paid=amount_paid)
            order.save()
            # get order items info
            for product_id, product_qty in cart_products_qty.items():
                # calculate item price
                price = cart.calculate_price(product=product_id,qty=product_qty)
                order_item = OrderItem(order=order, user=user, product=Product.objects.get(id=product_id), quantity=product_qty, price=price)
                order_item.save()

        # created order items for loggend in users 
        else:
            #not logged in
            # created order for anonymous users 
            order = Order(full_name=full_name, email=email, ShippingAddress=my_address, amount_paid=amount_paid)
            order.save()
            # create order items for anonymous users
            for product_id, product_qty in cart_products_qty.items():
                # calculate item price
                price = cart.calculate_price(product=product_id,qty=product_qty)
                order_item = OrderItem(order=order, product=Product.objects.get(id=product_id), quantity=product_qty, price= price)
                order_item.save()
        # Delete our cart
        cart.delete_cart()

        # Delete Cart from Database (old_cart field)
        current_user = Profile.objects.filter(user__id=request.user.id)
        # Delete shopping cart in database (old_cart field)
        current_user.update(old_cart="")
     

        messages.error(request, 'Order Places')
        return redirect('index')

    else:
        messages.error(request, 'Access Denied!')
        return redirect('index')
    
def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        shipped_items = Order.objects.filter(shipped=True)
        return render(request, "payment/shipped_dash.html", {'shipped_itmes': shipped_items})
    else:
        messages.error(request, 'Access Denied')
        return redirect('index')


def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        un_shipped_items = Order.objects.filter(shipped=False)
        return render(request, "payment/not_shipped_dash.html", {'un_shipped_items': un_shipped_items})
    
    
def orders(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        # get the order
        order = Order.objects.get(id=pk)
        # get order items
        order_items = OrderItem.objects.filter(order=pk)

        if request.POST:
            status = request.POST['shipping_status']
            # Check if true or false
            if status == "true":
                # Get the order
                order = Order.objects.filter(id=pk)
                # Update the status
                now = datetime.datetime.now()
                order.update(shipped=True, date_shipped=now)
            else:
                # Get the order
                order = Order.objects.filter(id=pk)
                # Update the status
                order.update(shipped=False)
            messages.success(request, "Shipping Status Updated")
            return redirect('index')

        return render(request, 'payment/orders.html', {'order': order, 'order_items':order_items})

    else:
        messages.error(request, 'Access Denied')
        return redirect('index')
    
