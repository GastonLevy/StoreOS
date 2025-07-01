from django.db import models
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from .supplier_model import Supplier
from inventory.models import Item
from users.models import Company

class SupplierEntry(models.Model):
    supplier = models.ForeignKey(Supplier, related_name='entries', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, related_name='supplier_entries', on_delete=models.SET_NULL, null=True, blank=True)
    item_name = models.CharField(max_length=255, blank=True, null=True)
    item_code = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.IntegerField()  # Cantidad ingresada
    comment = models.TextField(blank=True, null=True)  # Comentario adicional
    date = models.DateTimeField(auto_now_add=True)  # Fecha de creación
    expiration_date = models.DateField(verbose_name="Fecha de Caducidad", blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Costo", blank=True, null=True)
    company = models.ForeignKey(Company, related_name='supplier_entries', on_delete=models.CASCADE)  # Relación con la compañía

    def clean(self):
        if self.expiration_date and self.expiration_date < now().date():
            raise ValidationError("La fecha de caducidad no puede ser anterior a la fecha actual.")
        super().clean()

    def save(self, *args, **kwargs):
        if self.item:
            self.item_name = self.item.name
            self.item_code = self.item.barcode
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} de {self.item_name or 'Sin ítem'} por {self.supplier.name} - {self.date}"
