from django.db import models
from django.contrib.auth.models import User

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