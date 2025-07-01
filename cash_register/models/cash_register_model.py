from django.db import models
from django.conf import settings
from users.models.company_model import Company  # Import your company model
from checkout.models.cart_model import Cart  # Import cart model

class CashRegister(models.Model):
    """
    Represents a cash register session associated with a user and company.

    Attributes:
        user (ForeignKey): User owning the cash register.
        company (ForeignKey): Company of the cash register.
        status (str): Status of the register, 'abierta' (open) or 'cerrada' (closed).
        opening_balance (Decimal): Initial balance when opening the register.
        closing_balance (Decimal, optional): Final balance when closing the register.
        created_at (DateTime): Timestamp of when the register was opened.
        closed_at (DateTime, optional): Timestamp of when the register was closed.
        carts (ManyToMany): Related carts linked to this cash register.

    Returns:
        str: String representation with user and register status.

    Raises:
        None explicitly.
    """

    STATUS_CHOICES = [
        ('abierta', 'Abierta'),
        ('cerrada', 'Cerrada'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cash_registers')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='cash_registers')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='abierta')
    opening_balance = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Initial Balance")
    closing_balance = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Closing Balance", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Opening Date")
    closed_at = models.DateTimeField(null=True, blank=True, verbose_name="Closing Date")
    carts = models.ManyToManyField(Cart, blank=True, related_name='cash_registers')

    def __str__(self):
        return f"Cash Register of {self.user.username} - {self.get_status_display()}"

    def calculate_total(self):
        """
        Calculates the total balance based on completed carts and cash movements.

        Returns:
            Decimal: The calculated total balance.

        Raises:
            None explicitly.
        """
        # Sum of completed carts total prices
        sales = sum(cart.total_price() for cart in self.carts.filter(is_completed=True))
        # Sum of income movements
        total_income = sum(m.amount for m in self.movements.filter(type='ingreso'))
        # Sum of expense movements
        total_expense = sum(m.amount for m in self.movements.filter(type='egreso'))

        return self.opening_balance + sales + total_income - total_expense
