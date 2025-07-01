from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from users.models import Company

class ActionLog(models.Model):
    """
    Model to log actions performed on other watched models,
    such as creation, editing, or deletion.
    """
    ACTION_CHOICES = [
        ('CREATE', 'Creación'),
        ('EDIT', 'Edición'),
        ('DELETE', 'Eliminación'),
    ]

    company = models.ForeignKey(
        Company,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='logs',
        help_text="Empresa asociada a la acción (si aplica)."
    )
    user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="Usuario que realizó la acción."
    )
    action = models.CharField(
        max_length=10,
        choices=ACTION_CHOICES,
        help_text="Tipo de acción realizada."
    )
    model_name = models.CharField(
        max_length=255,
        help_text="Nombre del modelo donde se realizó la acción."
    )
    object_id = models.PositiveIntegerField(
        help_text="ID del objeto afectado."
    )
    timestamp = models.DateTimeField(
        default=now,
        help_text="Fecha y hora de la acción."
    )
    details = models.TextField(
        help_text="Descripción detallada de los datos afectados (antes/después)."
    )

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.action} en {self.model_name} por {self.user} ({self.timestamp})"
