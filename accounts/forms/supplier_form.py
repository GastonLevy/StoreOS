from django import forms
from ..models import Supplier

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'contact', 'email', 'phone', 'address', 'receipt']
        labels = {
            'name': 'Nombre del Proveedor',
            'contact': 'Contacto',
            'email': 'Correo Electrónico',
            'phone': 'Teléfono',
            'address': 'Dirección',
            'receipt': 'Remito (PDF/Imagen)',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'receipt': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
