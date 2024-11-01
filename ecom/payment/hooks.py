from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver
from django.conf import settings

@receiver(valid_ipn_received)
def paypal_payment_Recieved(sender, **kwargs):
    # grab the info that paypal sends 
    paypal_obj = sender
    
