from django.db import models
from users.models.company_model import Company

class PaymentMethod(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nombre del método de pago")
    description = models.TextField(blank=True, null=True, verbose_name="Descripción")
    is_active = models.BooleanField(default=True, verbose_name="Activo")

    def __str__(self):
        return self.name
