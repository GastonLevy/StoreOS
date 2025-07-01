from django.db import models
from ckeditor.fields import RichTextField
from .wiki_category_model import WikiCategory

class WikiEntry(models.Model):
    """
    Model representing a wiki entry or article.

    Attributes:
        title (CharField): Entry title.
        content (RichTextField): Rich content using CKEditor.
        category (ForeignKey): Relation to the category it belongs to.
        created_at (DateTimeField): Automatic creation timestamp.
        updated_at (DateTimeField): Automatic last update timestamp.
    """
    title = models.CharField(max_length=200)
    content = RichTextField()
    category = models.ForeignKey(
        WikiCategory, related_name='entries', on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
