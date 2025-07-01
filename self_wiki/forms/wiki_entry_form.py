from django import forms
from ..models import WikiEntry
from ckeditor.widgets import CKEditorWidget

class WikiEntryForm(forms.ModelForm):
    """
    Form for creating and editing wiki entries,
    using CKEditor for the content field.
    """
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = WikiEntry
        fields = ['title', 'content', 'category']
