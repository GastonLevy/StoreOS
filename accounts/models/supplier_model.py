from django.db import models
from users.models import Company

class Supplier(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nombre del Proveedor")
    contact = models.CharField(max_length=100, verbose_name="Contacto", blank=True, null=True)
    email = models.EmailField(verbose_name="Correo Electrónico", blank=True, null=True)
    phone = models.CharField(max_length=20, verbose_name="Teléfono", blank=True, null=True)
    address = models.TextField(verbose_name="Dirección", blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='suppliers')
    
    # Campo para cargar el archivo (puede ser PDF, imagen, etc.)
    receipt = models.FileField(upload_to='suppliers/receipts/', null=True, blank=True, verbose_name="Remito")

    def __str__(self):
        return self.name
