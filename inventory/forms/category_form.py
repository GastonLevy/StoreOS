from django import forms
from ..models import Category

class CategoryForm(forms.ModelForm):
    """
    Form for creating and updating Category instances with validation.

    Methods:
        clean_name() -> str:
            Validates that the category name is not longer than 100 characters
            and that it does not already exist in the company.

            Raises:
                ValidationError: If name exceeds 100 characters or if category already exists.
            
            Returns:
                str: The validated category name.
    """
    class Meta:
        model = Category
        fields = ['name']  # Only 'name' field is needed
        labels = {
            'name': 'Nombre de la categoría'  # Change label for 'name'
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')

        # Check length of the name
        if len(name) > 100:
            raise forms.ValidationError('El nombre de la categoría no puede exceder los 100 caracteres.')

        # Check for duplicates in the same company
        user_profile = getattr(self, 'user_profile', None)  # Avoid error if user_profile is not passed
        if user_profile:
            if Category.objects.filter(name=name, company=user_profile.company).exists():
                raise forms.ValidationError('La categoría ya existe.')

        return name
