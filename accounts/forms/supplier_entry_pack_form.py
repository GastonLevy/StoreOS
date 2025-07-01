from django import forms
from ..models import EntryPack, SupplierEntry

class EntryPackForm(forms.ModelForm):
    """
    Form for creating or updating EntryPack instances.

    Attributes:
        entries (ModelMultipleChoiceField): Optional field for selecting multiple SupplierEntry objects.

    Meta:
        model (EntryPack): The model this form is associated with.
        fields (list): Fields included in the form - 'description' and 'entries'.
        widgets (dict): Custom widgets for form fields.

    Raises:
        None explicitly.
    """

    entries = forms.ModelMultipleChoiceField(
        queryset=SupplierEntry.objects.none(),
        required=False
    )  # Make 'entries' optional

    class Meta:
        model = EntryPack
        fields = ['description', 'entries']
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Agrega una descripción opcional',
                'rows': 3
            }),
            'entries': forms.SelectMultiple(attrs={
                'class': 'form-control',
            }),
        }
