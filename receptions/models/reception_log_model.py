from django.db import models
from .reception_model import Reception
from users.models import Company

class ReceptionLog(models.Model):
    """
    Model representing a log entry for a Reception.

    Attributes:
        reception (Reception): Related reception instance.
        timestamp (datetime): Date and time when the log entry was created.
        description (str): Description of the log entry.
        user (User): User who created the log entry, nullable.
        company (Company): Related company.

    Methods:
        __str__(): Returns a readable string representation of the log entry.
    """

    reception = models.ForeignKey(
        Reception,
        on_delete=models.CASCADE,
        related_name='logs',
        verbose_name="Recepción"
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha y hora"
    )
    description = models.TextField(
        verbose_name="Descripción"
    )
    user = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Usuario"
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='receptionLogs'
    )

    def __str__(self):
        """
        Returns a readable string representation of the ReceptionLog instance.

        Returns:
            str: String showing related reception and date of the log.
        """
        return f"Log for {self.reception} - {self.timestamp.strftime('%Y-%m-%d')}"
