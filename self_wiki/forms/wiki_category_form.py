from django import forms
from ..models import WikiCategory

class WikiCategoryForm(forms.ModelForm):
    """
    Form for creating and editing wiki categories.
    """
    class Meta:
        model = WikiCategory
        fields = ['name', 'description']
