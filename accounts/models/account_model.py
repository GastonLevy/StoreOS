from django.db import models
from django.db.models import Sum
from users.models import Company


class Person(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="Nombre")
    last_name = models.CharField(max_length=50, verbose_name="Apellido")
    dni = models.CharField(max_length=20, blank=True, null=True, verbose_name="DNI")
    phone = models.CharField(max_length=20, verbose_name="Teléfono", blank=True, null=True)
    address = models.TextField(verbose_name="Dirección", blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="persons")

    class Meta:
        unique_together = ('company', 'dni')

    def total_debt(self):
        """
        Calculate total balance:
        - Debts linked to carts with payment method 'Cuenta Corriente'
        - Debts without cart
        """
        debts = self.debts.filter(
            models.Q(cart__isnull=True) |
            models.Q(cart__payment_method__name="Cuenta Corriente")
        )

        return debts.aggregate(total=Sum('amount'))['total'] or 0

    def __str__(self):
        return f"{self.first_name} {self.last_name}"