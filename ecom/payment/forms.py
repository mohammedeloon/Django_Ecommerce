from django import forms
from .models import ShippingAddress

class ShippingForm(forms.ModelForm):
    shipping_full_name = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'full_name'}), required=True)
    shipping_email = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'shipping_email'}), required=True)
    shipping_address1 = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'shipping_address1'}), required=True)
    shipping_address2 = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'shipping_address2'}), required=True)
    shipping_city = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'shipping_city'}), required=True)
    shipping_state = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'shipping_state'}))
    shipping_zipcode = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'shipping_zipcode'}))
    shipping_country = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'shipping_country'}), required=True)

    class Meta:
        model = ShippingAddress
        fields = ['shipping_full_name', 'shipping_email', 'shipping_address1', 'shipping_address2', 'shipping_city', 'shipping_state',
                  'shipping_zipcode','shipping_country', ]
        exculde = ['user', ]

class PaymentForm(forms.Form):
    card_name =  forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Name on Card'}), required=True)
    card_number = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'card Number'}), required=True)
    card_expiration_date = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Expiary Date'}), required=True)
    card_cvv_number = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'CVV'}), required=True)
    card_address1 = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Address 1'}), required=True)
    card_address2 = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Address 2'}), required=True)
    card_city = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'City'}), required=True)
    card_state = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'State'}), required=True)
    card_zipcode = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Zip Code'}), required=True)
    card_country = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Country'}), required=True)
        