from django.db import models
from django.contrib.auth.models import User
from users.models.company_model import Company
from .payment_method_model import PaymentMethod
from django.core.validators import MinValueValidator

class Cart(models.Model):
    """
    Represents a shopping cart associated with a user and company.

    Attributes:
        user (User or None): The user who owns the cart. Can be null for anonymous carts.
        company (Company): The company associated with the cart.
        payment_method (PaymentMethod or None): The payment method used, optional.
        payment_return (Decimal or None): Amount returned to the customer, must be >= 0.
        is_completed (bool): Indicates if the cart checkout is completed.
        created_at (datetime): Timestamp of cart creation.
        updated_at (datetime): Timestamp of last cart update.
        paid_amount (Decimal or None): Amount paid for the cart, defaults to 0.
        client (Person or None): Optional client linked to the cart.

    Methods:
        total_price() -> Decimal:
            Calculates and returns the total price of all cart lines.

    Raises:
        No explicit raises.
    """

    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='carts')  # Relation to User
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='carts')  # Relation to Company
    payment_method = models.ForeignKey(PaymentMethod, null=True, blank=True, on_delete=models.SET_NULL, related_name='carts')  # Relation to PaymentMethod
    payment_return = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)]
    )
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    client = models.ForeignKey('accounts.Person', null=True, blank=True, on_delete=models.CASCADE, related_name='carts')  # Use string notation to avoid circular import

    def __str__(self):
        return f"Cart {self.id} - User: {self.user if self.user else 'Anonymous'} - Company: {self.company.name}"

    def total_price(self):
        """
        Calculate the total price of the cart by summing the total of each cart line.

        Returns:
            Decimal: The sum of all cart lines' total prices.
        """
        total = sum(item.total for item in self.cart_lines.all())
        return total
