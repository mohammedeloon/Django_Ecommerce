from django.db import models
from django.contrib.auth.models import User
from store.models import Product
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import datetime

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=225)
    shipping_email = models.CharField(max_length=225)
    shipping_address1 = models.CharField(max_length=225)
    shipping_address2 = models.CharField(max_length=225)
    shipping_city = models.CharField(max_length=225)
    shipping_state = models.CharField(max_length=225, null=True, blank=True)
    shipping_zipcode = models.CharField(max_length=225, null=True, blank=True)
    shipping_country = models.CharField(max_length=225)

    def __str__(self) -> str:
        return f"Shipping Address = {str(self.id)}"

    # Do not pluralize model name 
    class Meta:
        verbose_name_plural = 'ShippingAddress'

# create a user profile by default when a user signs up
def create_shipping_address(sender, instance, created, **kwargs):
    if created:
        user_profile = ShippingAddress(user=instance)
        user_profile.save()

# automate the profile creation
post_save.connect(create_shipping_address, sender=User)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=250)
    email = models.CharField(max_length=250)
    ShippingAddress = models.TextField(max_length=1000)
    amount_paid = models.DecimalField(max_digits=7, decimal_places=2)
    date_ordered = models.DateTimeField(auto_now_add=True)
    shipped = models.BooleanField(default=False)
    date_shipped = models.DateField(blank=True, null=True)

    def __str__(self) -> str:
        return f'order - {str(self.id)}'

# Auto Add shipping Date
@receiver(pre_save, sender=Order)
def set_shipped_date_on_update(sender, instance, **kwargs):
	if instance.pk:
		now = datetime.datetime.now()
		obj = sender._default_manager.get(pk=instance.pk)
		if instance.shipped and not obj.shipped:
			instance.date_shipped = now


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self) -> str:
        return f'order item - {str(self.id)}'

