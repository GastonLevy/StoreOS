from django.db import models
from checkout.models.payment_method_model import PaymentMethod  # Import payment method model
from checkout.models.cart_model import Cart  # Import cart model
from .cash_register_model import CashRegister  # Import cash register model
from users.models.company_model import Company

class CashMovement(models.Model):
    """
    Represents a cash movement (income or expense) linked to a cash register.

    Attributes:
        cash_register (ForeignKey): Related cash register instance.
        payment_method (ForeignKey): Payment method used.
        type (str): Movement type, 'ingreso' (income) or 'egreso' (expense).
        amount (Decimal): Amount of the movement.
        description (str, optional): Description of the movement.
        cart (ForeignKey, optional): Related cart, if any.
        created_at (DateTime): Timestamp when the movement was created.
        company (ForeignKey): Company to which this movement belongs.

    Returns:
        str: String representation showing movement type and amount.

    Raises:
        None explicitly.
    """

    MOVEMENT_TYPE_CHOICES = [
        ('ingreso', 'Ingreso'),
        ('egreso', 'Egreso'),
    ]
    
    cash_register = models.ForeignKey(CashRegister, on_delete=models.CASCADE, related_name='movements')
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE, verbose_name="Payment Method")
    type = models.CharField(max_length=10, choices=MOVEMENT_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    cart = models.ForeignKey(Cart, null=True, blank=True, on_delete=models.SET_NULL, related_name='movements')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Movement Date")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="CashMovements")

    def __str__(self):
        return f"{self.get_type_display()} - {self.amount}"
