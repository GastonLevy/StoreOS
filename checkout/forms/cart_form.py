# checkout/forms.py
from django import forms
from ..models import Cart

class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = []  # No necesitamos campos porque el carrito se asocia automáticamente con el usuario y la compañía
