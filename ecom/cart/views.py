from django.shortcuts import render, redirect


def cart_summary(request):
    return render(request, 'cart_summary.html', {})

def add_cart(request):
    pass

def update_cart(request):
    pass

def delete_cart(request):
    pass