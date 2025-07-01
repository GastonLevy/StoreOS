from django.db import models
from users.models import Company
from .supplier_model import Supplier
from .supplier_entry_model import SupplierEntry  # Importa el modelo SupplierEntry

class EntryPack(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name="entry_packs", verbose_name="Proveedor")
    description = models.TextField(blank=True, null=True, verbose_name="Descripción")
    entries = models.ManyToManyField(SupplierEntry, related_name="packs", verbose_name="Entradas")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="entry_packs", verbose_name="Compañía")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")

    def __str__(self):
        return f"Pack #{self.id} - {self.created_at.strftime('%Y-%m-%d')}"

