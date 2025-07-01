# cyber_control/models/device_model.py
from django.db import models
from users.models import Company

class Device(models.Model):
    name = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='devices')

    def __str__(self):
        return self.name
