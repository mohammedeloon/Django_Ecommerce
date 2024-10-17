from django.urls import path 
from . import views


urlpatterns = [
    path('payment_success/', views.payment_success, name='payment_success'),
    path('checkout/', views.check_out, name='check_out'),
]