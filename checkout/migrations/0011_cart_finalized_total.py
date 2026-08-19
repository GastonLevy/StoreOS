# Generated manually for cash register payment method totals.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0010_remove_cart_cash_register'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='finalized_total',
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=10,
                null=True,
            ),
        ),
    ]
