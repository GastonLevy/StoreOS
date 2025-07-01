from django import forms
from ..models.cash_register_model import CashRegister

MAX_OPENING_BALANCE = 99999999.99  # Maximum allowed opening balance

class OpenCashRegisterForm(forms.ModelForm):
    """
    Form to open a new cash register session.

    Args:
        user (User): The user opening the cash register, passed via kwargs.

    Fields:
        opening_balance (Decimal): Initial balance for the cash register.

    Raises:
        ValidationError: If the opening_balance exceeds the maximum allowed value.
        ValidationError: If the user already has an open cash register.

    Returns:
        cleaned_data (dict): Validated form data.
    """

    class Meta:
        model = CashRegister
        fields = ['opening_balance']

    def __init__(self, *args, **kwargs):
        # Get the user from kwargs for validation
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean_opening_balance(self):
        # Validate the opening balance does not exceed maximum allowed value
        opening_balance = self.cleaned_data.get('opening_balance')
        if opening_balance > MAX_OPENING_BALANCE:
            raise forms.ValidationError(
                f'El saldo inicial no puede superar {MAX_OPENING_BALANCE}.'
            )
        return opening_balance

    def clean(self):
        # Validate that the user doesn't already have an open cash register
        cleaned_data = super().clean()
        if CashRegister.objects.filter(user=self.user, status='abierta').exists():
            raise forms.ValidationError("El usuario ya tiene una caja abierta.")
        return cleaned_data
