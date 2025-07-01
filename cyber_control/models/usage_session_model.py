from django.db import models
from django.utils.timezone import now, timedelta
from users.models import Company
from accounts.models import Person
from .device_model import Device

class UsageSession(models.Model):
    """
    Represents a usage session for a device.

    Attributes:
        device (ForeignKey): The device being used.
        client (ForeignKey, optional): The client using the device; can be null.
        company (ForeignKey): The company that owns the device/session.
        start_time (DateTimeField): The start datetime of the session.
        duration (DurationField): Duration of the session (e.g., 2 hours).
        total_duration (DurationField): Total accumulated duration.
        end_time (DateTimeField, optional): Calculated end time of the session.
        is_active (BooleanField): Indicates if the session is currently active.

    Methods:
        save(*args, **kwargs): Overrides save to update end_time based on total_duration.

    Returns:
        None

    Raises:
        None
    """
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='usage_sessions')
    client = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='usage_sessions', null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='usage_sessions')
    start_time = models.DateTimeField(default=now)
    duration = models.DurationField(help_text="Duration in time format (e.g., 2 hours)")
    total_duration = models.DurationField(default=timedelta(), help_text="Accumulated total duration")
    end_time = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Recalculate end_time every time the object is saved based on total_duration
        if self.total_duration:
            self.end_time = self.start_time + self.total_duration
        super().save(*args, **kwargs)

    def __str__(self):
        client_name = self.client.name if self.client else "Sin cliente"
        return f"{self.device.name} - {client_name} - {self.start_time}"
