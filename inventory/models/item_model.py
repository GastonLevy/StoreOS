from django.db import models
from django.core.validators import MinValueValidator
from .category_model import Category
from users.models import Company

class Item(models.Model):
    """
    Represents an inventory item.

    Attributes:
        name (str): Name of the item.
        barcode (str, optional): Barcode identifier.
        price (Decimal): Price of the item, non-negative.
        quantity (int): Quantity in stock, can be negative.
        stockable (bool): Indicates if the item is stock-managed.
        description (str): Optional description.
        categories (ManyToMany): Related categories.
        company (ForeignKey): Company owning the item.
        cost (Decimal): Cost charged by the supplier, non-negative.
        hide (bool): Whether to hide the item in lists and searches.

    Methods:
        __str__: Returns the item's name.
    """
    name = models.CharField(max_length=100)
    barcode = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Precio del artículo"
    )

    # Changed from PositiveIntegerField to IntegerField to allow negative values
    quantity = models.IntegerField()

    stockable = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    categories = models.ManyToManyField(Category, related_name='items', blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='items')

    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=0.00,
        help_text="Costo que el proveedor cobra por el artículo"
    )
    hide = models.BooleanField(
        default=False,
        help_text="Ocultar el ítem en listas y búsquedas"
    )

    def __str__(self):
        return self.name
