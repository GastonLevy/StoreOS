from django import forms
from ..models.cash_register_model import CashRegister

class CloseCashRegisterForm(forms.ModelForm):
    """
    Form to close an existing cash register session.

    Fields:
        closing_balance (Decimal): Final balance to close the cash register.

    Raises:
        ValidationError: If the closing_balance is negative.

    Returns:
        cleaned_data (dict): Validated form data.
    """

    class Meta:
        model = CashRegister
        fields = ['closing_balance']

    def clean_closing_balance(self):
        # Validate the closing balance is not negative
        closing_balance = self.cleaned_data.get('closing_balance')
        if closing_balance is not None and closing_balance < 0:
            raise forms.ValidationError("El saldo final no puede ser negativo.")
        return closing_balance
