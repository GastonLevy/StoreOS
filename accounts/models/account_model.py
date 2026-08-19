from django.db import models
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
        total = 0

        for debt in self.debts.select_related('cart'):
            if debt.cart is None:
                total += debt.amount
            elif (
                debt.status == 'pendiente'
                and debt.cart.is_current_account_sale
            ):
                total += debt.amount

        return total

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
