from django import forms
from ..models import Debt

class DebtUpdateForm(forms.ModelForm):
    class Meta:
        model = Debt
        fields = ['amount', 'due_date']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
