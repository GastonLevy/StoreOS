from django.conf import settings
from django.db import models
from .company_model import Company

class UserProfile(models.Model):
    """
    Perfil extendido del usuario que permite asociarlo a una empresa.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        help_text="Usuario asociado a este perfil"
    )
    company = models.ForeignKey(
        Company, 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True,
        help_text="Empresa a la que pertenece el usuario (opcional)"
    )

    def __str__(self):
        return f"Perfil de {self.user.username}"

    class Meta:
        ordering = ['user']
