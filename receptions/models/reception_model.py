from django.db import models
from users.models import Company
from accounts.models import Person
import uuid

class Reception(models.Model):
    """
    Model representing a Reception entry.

    Attributes:
        person (Person): Related person, optional.
        item (str): Name of the item.
        item_details (str): Details about the item, optional.
        reception_date (datetime): Date and time when reception was created.
        notes (str): Additional notes, optional.
        status (str): Current status of the reception ('pending' or 'completed').
        received_by (User): User who received the item, nullable.
        company (Company): Related company.
        auth_code (str): Unique authentication code, auto-generated if not set.

    Methods:
        save(*args, **kwargs): Overrides save to auto-generate auth_code if missing.
        __str__(): Returns a readable string representation.
    """

    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name='receptions',
        verbose_name="Person",
        null=True,
        blank=True
    )
    item = models.CharField(
        max_length=255,
        verbose_name="Item"
    )
    item_details = models.TextField(
        blank=True,
        null=True,
        verbose_name="Item details"
    )
    reception_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Reception date"
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name="Notes"
    )
    status = models.CharField(
        max_length=50,
        choices=[
            ('pending', "Pending"),
            ('completed', "Completed"),
        ],
        default='pending',
        verbose_name="Status"
    )
    received_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Received by"
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='receptions'
    )
    auth_code = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        null=True,
        verbose_name="Authentication code"
    )

    def save(self, *args, **kwargs):
        """
        Overrides save method to generate a unique auth_code if not already set.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            None
        """
        if not self.auth_code:
            self.auth_code = str(uuid.uuid4()).replace('-', '')[:12]  # Generate unique code
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Returns a readable string representation of the Reception instance.

        Returns:
            str: Formatted string with reception id, item, and person.
        """
        return f"Reception #{self.id} - {self.item} ({self.person})"
