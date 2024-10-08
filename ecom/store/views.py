from django.shortcuts import render, redirect
from .models import Category, Product
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django import forms
from django.contrib import messages


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
                username = form.cleaned_data.get('username')
                messages.success(request, f'An account has been created for user {username}!')
            else:
                messages.success(request, ('ops! There was a problem registering the user. Please, try again.'))
    
        return render(request, 'register.html', {'form': form})
        
def logout_user(request):
    logout(request)
    messages.success(request, ('Logged Out Successfully'))
    return redirect('index')
