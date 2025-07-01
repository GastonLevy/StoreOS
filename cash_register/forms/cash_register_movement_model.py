from django import forms
from ..models import CashMovement

class CashMovementForm(forms.ModelForm):
    """
    Form to create or update a CashMovement instance.

    Fields:
        type (str): Type of movement, e.g. 'ingreso' or 'egreso'.
        amount (Decimal): Amount of money moved.
        description (str, optional): Optional description of the movement.

    Returns:
        cleaned_data (dict): Validated form data.

    Raises:
        ValidationError: If any field validation fails (handled by Django forms).
    """

    class Meta:
        model = CashMovement
        fields = ['type', 'amount', 'description']
        labels = {
            'type': 'Tipo de Movimiento',
            'amount': 'Monto',
            'description': 'Descripción',
        }
        widgets = {
            # Use RadioSelect widget without empty option for 'type'
            'type': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el monto'}),
            'description': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Descripción opcional'
            }),
        }
