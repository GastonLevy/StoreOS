from django import forms
from ..models import Debt
from django.core.exceptions import ValidationError
from datetime import date

class DebtForm(forms.ModelForm):
    """
    Form to create or update a Debt instance.

    Fields:
        person (ForeignKey): The person related to the debt.
        amount (Decimal): The debt amount; must be positive.
        due_date (date): The due date; cannot be in the past.

    Methods:
        clean_amount():
            Validates that the amount is positive.
        clean_due_date():
            Validates that the due date is not before today.

    Raises:
        ValidationError: If amount is <= 0 or due_date is in the past.

    Returns:
        Cleaned data for amount and due_date fields.
    """

    class Meta:
        model = Debt
        fields = ['person', 'amount', 'due_date']
        labels = {
            'person': 'Persona',
            'amount': 'Monto',
            'due_date': 'Fecha de vencimiento',
        }
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'person': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_amount(self):
        """
        Validate that amount is positive.

        Returns:
            float: Cleaned positive amount.

        Raises:
            ValidationError: If amount is less or equal to zero.
        """
        amount = self.cleaned_data.get('amount')
        if amount is not None and amount <= 0:
            raise ValidationError("El monto debe ser un valor positivo.")
        return amount

    def clean_due_date(self):
        """
        Validate that due_date is not earlier than today.

        Returns:
            date: Cleaned due_date.

        Raises:
            ValidationError: If due_date is before today.
        """
        due_date = self.cleaned_data.get('due_date')
        if due_date and due_date < date.today():
            raise ValidationError("La fecha de vencimiento no puede ser anterior a hoy.")
        return due_date
