from django.db import models
from django.contrib.auth.models import User

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=225)
    email = models.CharField(max_length=225)
    address1 = models.CharField(max_length=225)
    address2 = models.CharField(max_length=225)
    city = models.CharField(max_length=225)
    state = models.CharField(max_length=225, null=True, blank=True)
    zipcode = models.CharField(max_length=225, null=True, blank=True)
    country = models.CharField(max_length=225)

    def __str__(self) -> str:
        return f"Shipping Address = {str(self.id)}"

    # Do not pluralize model name 
    class Meta:
        verbose_name_plural = 'ShippingAddress'