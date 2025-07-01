from django.db import models
from .account_model import Person
from checkout.models.cart_model import Cart
from users.models import Company

class Debt(models.Model):
    DEBT_STATUS_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
        ('cancelado', 'Cancelado'),
    ]
    
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='debts')  # Esto es correcto
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=DEBT_STATUS_CHOICES, default='pendiente')
    cart = models.ForeignKey(Cart, null=True, blank=True, on_delete=models.SET_NULL, related_name='debts')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="Debts")

    def __str__(self):
        return f"Deuda de {self.person} - {self.get_status_display()}"
