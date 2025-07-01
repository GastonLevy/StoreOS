from django import forms
from ..models import Reception
from accounts.models import Person

class ReceptionForm(forms.ModelForm):
    new_person_first_name = forms.CharField(max_length=50, required=False, label="Nombre")
    new_person_last_name = forms.CharField(max_length=50, required=False, label="Apellido")
    new_person_address = forms.CharField(max_length=255, required=False, label="Dirección")
    new_person_phone = forms.CharField(max_length=20, required=False, label="Teléfono")
    
    person_choice = forms.ChoiceField(choices=[('existing', 'Cliente Existente'), ('new', 'Crear Nuevo')], required=True)

    class Meta:
        model = Reception
        fields = ['person', 'item', 'item_details', 'notes', 'status']

    def __init__(self, *args, user_profile=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_profile = user_profile  # Guardamos el perfil de usuario para acceso en clean()

        if self.user_profile and self.user_profile.company:
            self.fields['person'].queryset = Person.objects.filter(company=self.user_profile.company)  # Filtrar por empresa

    def clean(self):
        cleaned_data = super().clean()
        person = cleaned_data.get('person')
        new_person_first_name = cleaned_data.get('new_person_first_name')
        new_person_last_name = cleaned_data.get('new_person_last_name')
        new_person_address = cleaned_data.get('new_person_address')
        new_person_phone = cleaned_data.get('new_person_phone')
        person_choice = cleaned_data.get('person_choice')

        if person_choice == 'new':
            if not new_person_first_name or not new_person_last_name or not new_person_phone:
                raise forms.ValidationError('Debes ingresar al menos el nombre, apellido y teléfono para crear una nueva persona.')

            if not self.user_profile or not self.user_profile.company:
                raise forms.ValidationError('No se puede crear la persona porque el usuario no tiene una compañía asignada.')

            person = Person.objects.create(
                first_name=new_person_first_name,
                last_name=new_person_last_name,
                address=new_person_address,
                phone=new_person_phone,
                company=self.user_profile.company  # Asignar la compañía correctamente
            )
            cleaned_data['person'] = person  # Asignar la nueva persona al formulario

        elif person_choice == 'existing' and not person:
            raise forms.ValidationError('Debes seleccionar un cliente existente.')

        return cleaned_data
