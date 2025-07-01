from django.db import models
from django.db.models import UniqueConstraint
from users.models import Company  # Asegúrate de que este sea el camino correcto

class Category(models.Model):
    name = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='categories')

    class Meta:
        constraints = [
            UniqueConstraint(fields=['name', 'company'], name='unique_name_per_company')
        ]

    def __str__(self):
        return self.name
