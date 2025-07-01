from django.db import models
from django.core.validators import MinValueValidator
from .cart_model import Cart
from inventory.models import Item
from users.models.company_model import Company

class CartLine(models.Model):
    """
    Represents a line item within a shopping cart.

    Attributes:
        cart (Cart): The cart this line belongs to.
        item (Item or None): The inventory item referenced; nullable if deleted.
        quantity (Decimal): The quantity of the item, must be > 0.
        price (Decimal): Unit price of the item in the cart.
        name (str): Name of the product at the time of adding to the cart.
        company (Company): The company associated with this cart line.

    Methods:
        save(*args, **kwargs):
            Saves the CartLine instance; sets price and name from the item if not provided.

    Properties:
        total (Decimal): Returns the total price for this line (quantity * price).

    Raises:
        ValidationError: If quantity is not greater than zero (enforced by validator).
    """

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_lines")
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, related_name="cart_lines", null=True)
    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        validators=[MinValueValidator(0.0001)]  # Ensure quantity is greater than 0
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Unit price of the item in the cart
    name = models.CharField(max_length=255)  # Product name stored to preserve even if Item is deleted
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='carts_lines')

    def __str__(self):
        return f"{self.quantity} x {self.name} in {self.cart.user.username if self.cart.user else 'Anonymous'}'s cart"

    def save(self, *args, **kwargs):
        # Use the item's price if no price is provided
        if not self.price and self.item:
            self.price = self.item.price

        # Use the item's name if no name is provided
        if not self.name and self.item:
            self.name = self.item.name

        super().save(*args, **kwargs)

    @property
    def total(self):
        """Calculate total price for this cart line."""
        return self.quantity * self.price
