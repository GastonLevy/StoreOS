from django.db import models
from users.models import Company

class Person(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="Nombre")
    last_name = models.CharField(max_length=50, verbose_name="Apellido")
    phone = models.CharField(max_length=20, verbose_name="Teléfono", blank=True, null=True)
    address = models.TextField(verbose_name="Dirección", blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="persons")

    def total_debt(self):
        """
        Calculate the total balance by summing debts related to a cart with the payment method 'Cuenta Corriente'
        or debts without any cart associated.

        Returns:
            float: The total amount of debt.

        Raises:
            None explicitly.
        """
        total = 0

        # Sum debts with a cart where payment method is 'Cuenta Corriente'
        debts_with_cart = self.debts.filter(cart__isnull=False)
        for debt in debts_with_cart:
            if debt.cart.payment_method.name == "Cuenta Corriente":
                total += debt.amount

        # Sum debts without a cart
        debts_without_cart = self.debts.filter(cart__isnull=True)
        for debt in debts_without_cart:
            total += debt.amount

        return total

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
