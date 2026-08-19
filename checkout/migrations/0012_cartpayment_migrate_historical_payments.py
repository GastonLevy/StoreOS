from decimal import Decimal

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


def cart_total(cart, CartLine):
    if cart.finalized_total is not None:
        return cart.finalized_total

    total = Decimal('0.00')
    for line in CartLine.objects.filter(cart_id=cart.pk):
        total += line.quantity * line.price

    return total.quantize(Decimal('0.01'))


def migrate_historical_payments(apps, schema_editor):
    Cart = apps.get_model('checkout', 'Cart')
    CartLine = apps.get_model('checkout', 'CartLine')
    CartPayment = apps.get_model('checkout', 'CartPayment')

    carts = (
        Cart.objects
        .filter(is_completed=True, payment_method__isnull=False)
        .select_related('payment_method')
    )

    for cart in carts.iterator():
        if CartPayment.objects.filter(cart_id=cart.pk).exists():
            continue

        amount = cart_total(cart, CartLine)

        if amount <= 0:
            continue

        received_amount = None
        change_amount = None

        if cart.payment_method.name == 'Efectivo':
            received_amount = cart.paid_amount
            change_amount = cart.payment_return

        CartPayment.objects.create(
            cart_id=cart.pk,
            payment_method_id=cart.payment_method_id,
            amount=amount,
            received_amount=received_amount,
            change_amount=change_amount,
        )


def reverse_historical_payments(apps, schema_editor):
    CartPayment = apps.get_model('checkout', 'CartPayment')
    CartPayment.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0011_cart_finalized_total'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartPayment',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'amount',
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=10,
                        validators=[
                            django.core.validators.MinValueValidator(
                                Decimal('0.01')
                            )
                        ],
                    ),
                ),
                (
                    'received_amount',
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=10,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(
                                Decimal('0.00')
                            )
                        ],
                    ),
                ),
                (
                    'change_amount',
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=10,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(
                                Decimal('0.00')
                            )
                        ],
                    ),
                ),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                (
                    'cart',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='payments',
                        to='checkout.cart',
                    ),
                ),
                (
                    'payment_method',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='cart_payments',
                        to='checkout.paymentmethod',
                    ),
                ),
            ],
            options={
                'ordering': ['created_at', 'id'],
            },
        ),
        migrations.RunPython(
            migrate_historical_payments,
            reverse_historical_payments,
        ),
    ]
