from django import forms
from ..models import Device

class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['name']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError('El nombre del dispositivo es obligatorio.')
        return name
