from django.db import models

class Company(models.Model):
    """
    Represents a company that can be associated with other models in the system.
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Nombre único de la empresa"
    )
    address = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Dirección de la empresa (opcional)"
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Empresas"
