from django.db import models

class WikiCategory(models.Model):
    """
    Model representing a category or topic within the wiki.

    Attributes:
        name (CharField): Unique name of the category.
        description (TextField): Optional description of the category.
    """
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)  # Can be optional

    def __str__(self):
        return self.name
