from django.shortcuts import render, redirect
from .models import Category, Product, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, UserInfoForm
from django import forms
from django.contrib import messages
from django.contrib.sessions.models import Session
import json
from cart.cart import Cart

def index(request):
    products = Product.objects.all() 
    return render(request, 'index.html', {'products':products})

def about(request):
    return render(request, 'about.html', {})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            current_user = Profile.objects.get(user__id= request.user.id)
            # get the saved cart from database
            saved_cart =  current_user.old_cart
            # check if there are some items in the saved cart 
            if saved_cart:
                # convert to dict using JSON
                saved_cart = json.loads(saved_cart)
                cart = Cart(request)
                # loop through the saved cart and add them from the database to the session again
                for key, value in saved_cart.items():
                    cart.db_add(product=key, quantity=value)



            messages.success(request, ('logged In Successfully'))
            return redirect('index')
        else:
            messages.success(request, ('There was an error! Try Again'))
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def register_user(request):
        form = SignUpForm()
        if request.method == "POST":
            form = SignUpForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                user = authenticate(username=username, password=password)
                # log in user
                user = authenticate(username=username, password=password)
                login(request, user)
                messages.success(request, 'Username Created! Please Continue the Sign Up Process')
                return redirect('update_info')
            else:
                messages.success(request, ('ops! There was a problem registering the user. Please, try again.'))
    
        return render(request, 'register.html', {'form': form})

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()
            login(request, current_user)
            messages.success(request, 'User Has Been Updated!')
            return redirect('index')
    
        return render(request, 'update_user.html', {'user_form':user_form})
    else:
        messages.success(request, 'You Must Be Logged in to Access that Page!')
        return redirect('index')
    
def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        form = UserInfoForm(request.POST or None, instance=current_user)

        if form.is_valid():
            form.save()
            messages.success(request, 'User Information Has Been Updated!')
            return redirect('index')
        
        return render(request, 'update_info.html', {'form': form})
    else:
        messages.success(request, 'You Must Be Logged in to Access that Page!')
        return redirect('index')
     
    
def update_password(request):
    # It has been made through Django built-in views (PasswordChangeView) called in the urls page directly
    pass

def logout_user(request):
    logout(request)
    messages.success(request, ('Logged Out Successfully'))
    return redirect('index')

def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product': product})

def search_product(request):
    query = request.GET.get('search')
    query = query.strip()
    products = None
    if query:
        products = Product.objects.filter(name__contains=query) | Product.objects.filter(description__contains=query)
    return render(request, 'search_product.html', {'products': products, 'query': query})
  
def category(request, foo):
    # Replace hyphens on links with space
    foo = foo.replace('-', ' ')
    try:
        category = Category.objects.get(name= foo)
        categories = Category.objects.all()
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products': products, 'category': category, 'categories': categories})

    except:
        messages.error(request, 'This category does not exist!')
        return redirect('index.html')
    
def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {'categories': categories})

