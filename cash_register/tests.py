from decimal import Decimal
from unittest.mock import patch

from django.contrib.auth.models import User
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpResponse
from django.test import RequestFactory, TestCase

from cash_register.models import CashRegister
from cash_register.views.detail_cash_register_view import cash_register_detail_view
from checkout.models import Cart, CartLine, PaymentMethod
from checkout.views.cart.cart_finalize_view import finalize_cart
from users.models import Company


class CashRegisterPaymentMethodTotalsTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.company = Company.objects.create(name='Test Store')
        self.user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='secret',
        )
        self.user.userprofile.company = self.company
        self.user.userprofile.save()

        self.cash = PaymentMethod.objects.create(name='Efectivo')
        self.mercado_pago = PaymentMethod.objects.create(name='Mercado Pago')

        self.cash_register = CashRegister.objects.create(
            user=self.user,
            company=self.company,
            opening_balance=Decimal('0.00'),
        )
        self.other_cash_register = CashRegister.objects.create(
            user=self.user,
            company=self.company,
            opening_balance=Decimal('0.00'),
        )

    def _create_completed_cart(
        self,
        cash_register,
        payment_method,
        finalized_total,
        line_amounts=None,
    ):
        cart = Cart.objects.create(
            user=self.user,
            company=self.company,
            payment_method=payment_method,
            is_completed=True,
            finalized_total=finalized_total,
        )
        cash_register.carts.add(cart)

        for index, line_amount in enumerate(line_amounts or [finalized_total]):
            CartLine.objects.create(
                cart=cart,
                item=None,
                quantity=Decimal('1.000'),
                price=line_amount,
                name=f'Item {index}',
                company=self.company,
            )

        return cart

    def _payment_method_totals_for(self, cash_register):
        request = self.factory.get('/cash_register/cash-register/detail/')
        request.user = self.user
        captured_context = {}

        def fake_render(request, template_name, context):
            captured_context.update(context)
            return HttpResponse('ok')

        with patch(
            'cash_register.views.detail_cash_register_view.render',
            side_effect=fake_render,
        ):
            cash_register_detail_view(request, cash_register.pk)

        return {
            payment['payment_method__name']: payment['total']
            for payment in captured_context['payment_method_totals']
        }

    def _add_session_and_messages(self, request):
        middleware = SessionMiddleware(lambda request: None)
        middleware.process_request(request)
        request.session.save()
        request._messages = FallbackStorage(request)

    def test_payment_method_totals_sum_multiple_sales_per_method(self):
        self._create_completed_cart(
            self.cash_register,
            self.cash,
            Decimal('10000.00'),
        )
        self._create_completed_cart(
            self.cash_register,
            self.cash,
            Decimal('19000.00'),
        )
        self._create_completed_cart(
            self.cash_register,
            self.mercado_pago,
            Decimal('6000.00'),
        )
        self._create_completed_cart(
            self.cash_register,
            self.mercado_pago,
            Decimal('3800.00'),
        )

        totals = self._payment_method_totals_for(self.cash_register)

        self.assertEqual(totals['Efectivo'], Decimal('29000.00'))
        self.assertEqual(totals['Mercado Pago'], Decimal('9800.00'))

    def test_cart_with_multiple_lines_is_counted_once(self):
        self._create_completed_cart(
            self.cash_register,
            self.mercado_pago,
            Decimal('9800.00'),
            line_amounts=[
                Decimal('5000.00'),
                Decimal('4800.00'),
            ],
        )

        totals = self._payment_method_totals_for(self.cash_register)

        self.assertEqual(totals['Mercado Pago'], Decimal('9800.00'))

    def test_sales_from_another_cash_register_are_not_included(self):
        self._create_completed_cart(
            self.cash_register,
            self.mercado_pago,
            Decimal('9800.00'),
        )
        self._create_completed_cart(
            self.other_cash_register,
            self.mercado_pago,
            Decimal('35400.00'),
        )

        totals = self._payment_method_totals_for(self.cash_register)

        self.assertEqual(totals['Mercado Pago'], Decimal('9800.00'))

    def test_payment_method_total_uses_finalized_total_after_line_changes(self):
        cart = self._create_completed_cart(
            self.cash_register,
            self.mercado_pago,
            Decimal('9800.00'),
        )
        line = cart.cart_lines.first()
        line.price = Decimal('45200.00')
        line.save()

        totals = self._payment_method_totals_for(self.cash_register)

        self.assertEqual(cart.total_price(), Decimal('45200.00000'))
        self.assertEqual(totals['Mercado Pago'], Decimal('9800.00'))

    def test_finalize_cart_stores_historical_total(self):
        cart = Cart.objects.create(
            user=self.user,
            company=self.company,
        )
        self.cash_register.carts.add(cart)
        self.other_cash_register.carts.add(cart)
        CartLine.objects.create(
            cart=cart,
            item=None,
            quantity=Decimal('2.000'),
            price=Decimal('1500.00'),
            name='Finalized item',
            company=self.company,
        )

        request = self.factory.post(
            '/checkout/cart/finalize/',
            {
                'payment_method': str(self.cash.pk),
                'paid_amount': '3000.00',
            },
        )
        request.user = self.user
        self._add_session_and_messages(request)

        finalize_cart(request, cart.pk)
        cart.refresh_from_db()

        self.assertTrue(cart.is_completed)
        self.assertEqual(cart.finalized_total, Decimal('3000.00'))
        self.assertEqual(
            list(cart.cash_registers.order_by('pk')),
            [self.cash_register],
        )
