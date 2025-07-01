from django import forms
from ..models import Reception

class ReceptionStatusForm(forms.ModelForm):
    class Meta:
        model = Reception
        fields = ['status']  # Solo se permitirá editar el estado
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
