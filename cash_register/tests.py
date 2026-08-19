from decimal import Decimal
from unittest.mock import patch

from django.contrib.auth.models import User
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.http import HttpResponse
from django.test import RequestFactory, TestCase, TransactionTestCase

from accounts.models import Debt, Person
from cash_register.context_processors.cash_register_status import cash_register_amount
from cash_register.models import CashRegister
from cash_register.views.detail_cash_register_view import cash_register_detail_view
from checkout.models import Cart, CartLine, CartPayment, PaymentMethod
from checkout.views.cart.cart_finalize_view import finalize_cart
from users.models import Company
import self_logs.signals as log_signals


class CashRegisterPaymentFlowTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.company = Company.objects.create(name='Test Store')
        self.other_company = Company.objects.create(name='Other Store')
        self.user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='secret',
        )
        self.user.userprofile.company = self.company
        self.user.userprofile.save()

        self.cash = PaymentMethod.objects.create(name='Efectivo')
        self.mercado_pago = PaymentMethod.objects.create(name='Mercado Pago')
        self.transfer = PaymentMethod.objects.create(name='Transferencia')
        self.current_account = PaymentMethod.objects.create(name='Cuenta Corriente')

        self.cash_register = CashRegister.objects.create(
            user=self.user,
            company=self.company,
            opening_balance=Decimal('1000.00'),
        )
        self.other_cash_register = CashRegister.objects.create(
            user=self.user,
            company=self.company,
            opening_balance=Decimal('0.00'),
        )
        self.client = Person.objects.create(
            first_name='Ada',
            last_name='Lovelace',
            company=self.company,
        )

    def _add_session_and_messages(self, request):
        middleware = SessionMiddleware(lambda request: None)
        middleware.process_request(request)
        request.session.save()
        request._messages = FallbackStorage(request)

    def _create_cart(self, total=Decimal('29800.00'), company=None):
        cart = Cart.objects.create(
            user=self.user,
            company=company or self.company,
        )
        self.cash_register.carts.add(cart)
        CartLine.objects.create(
            cart=cart,
            item=None,
            quantity=Decimal('1.000'),
            price=total,
            name='Sale item',
            company=company or self.company,
        )
        return cart

    def _finalize(self, cart, methods, amounts, received=None, person=None):
        data = {
            'payment_method': [str(method.pk) for method in methods],
            'payment_amount': [str(amount) for amount in amounts],
            'received_amount': [
                '' if value is None else str(value)
                for value in (received or [None] * len(methods))
            ],
        }

        if person:
            data['person'] = str(person.pk)

        request = self.factory.post(
            f'/checkout/cart/{cart.pk}/finalize/',
            data,
        )
        request.user = self.user
        self._add_session_and_messages(request)

        return finalize_cart(request, cart.pk)

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
        }, captured_context

    def test_sale_fully_paid_with_cash(self):
        cart = self._create_cart(Decimal('29800.00'))

        self._finalize(
            cart,
            [self.cash],
            [Decimal('29800.00')],
            [Decimal('30000.00')],
        )
        cart.refresh_from_db()

        payment = cart.payments.get()
        self.assertTrue(cart.is_completed)
        self.assertEqual(payment.amount, Decimal('29800.00'))
        self.assertEqual(payment.received_amount, Decimal('30000.00'))
        self.assertEqual(payment.change_amount, Decimal('200.00'))

    def test_sale_fully_paid_with_mercado_pago(self):
        cart = self._create_cart(Decimal('9800.00'))

        self._finalize(
            cart,
            [self.mercado_pago],
            [Decimal('9800.00')],
        )

        payment = cart.payments.get()
        self.assertEqual(payment.payment_method, self.mercado_pago)
        self.assertEqual(payment.amount, Decimal('9800.00'))
        self.assertIsNone(payment.received_amount)
        self.assertIsNone(payment.change_amount)

    def test_sale_paid_with_cash_and_mercado_pago(self):
        cart = self._create_cart(Decimal('29800.00'))

        self._finalize(
            cart,
            [self.cash, self.mercado_pago],
            [Decimal('20000.00'), Decimal('9800.00')],
            [Decimal('25000.00'), None],
        )

        payments = {
            payment.payment_method.name: payment
            for payment in cart.payments.select_related('payment_method')
        }
        self.assertEqual(payments['Efectivo'].amount, Decimal('20000.00'))
        self.assertEqual(payments['Efectivo'].change_amount, Decimal('5000.00'))
        self.assertEqual(payments['Mercado Pago'].amount, Decimal('9800.00'))

    def test_sale_paid_with_three_methods(self):
        cart = self._create_cart(Decimal('30000.00'))

        self._finalize(
            cart,
            [self.cash, self.mercado_pago, self.transfer],
            [Decimal('10000.00'), Decimal('9800.00'), Decimal('10200.00')],
            [Decimal('10000.00'), None, None],
        )

        self.assertEqual(cart.payments.count(), 3)
        self.assertEqual(cart.payments_total(), Decimal('30000.00'))

    def test_rejects_payment_sum_below_total(self):
        cart = self._create_cart(Decimal('29800.00'))

        self._finalize(
            cart,
            [self.cash, self.mercado_pago],
            [Decimal('10000.00'), Decimal('9800.00')],
            [Decimal('10000.00'), None],
        )
        cart.refresh_from_db()

        self.assertFalse(cart.is_completed)
        self.assertEqual(cart.payments.count(), 0)

    def test_rejects_payment_sum_above_total(self):
        cart = self._create_cart(Decimal('29800.00'))

        self._finalize(
            cart,
            [self.cash, self.mercado_pago],
            [Decimal('20000.00'), Decimal('10000.00')],
            [Decimal('20000.00'), None],
        )
        cart.refresh_from_db()

        self.assertFalse(cart.is_completed)
        self.assertEqual(cart.payments.count(), 0)

    def test_rejects_cash_received_below_applied_amount(self):
        cart = self._create_cart(Decimal('20000.00'))

        self._finalize(
            cart,
            [self.cash],
            [Decimal('20000.00')],
            [Decimal('19000.00')],
        )
        cart.refresh_from_db()

        self.assertFalse(cart.is_completed)
        self.assertEqual(cart.payments.count(), 0)

    def test_cash_register_report_groups_by_cart_payment_method(self):
        cart = self._create_cart(Decimal('29800.00'))
        self._finalize(
            cart,
            [self.cash, self.mercado_pago],
            [Decimal('20000.00'), Decimal('9800.00')],
            [Decimal('25000.00'), None],
        )

        totals, _ = self._payment_method_totals_for(self.cash_register)

        self.assertEqual(totals['Efectivo'], Decimal('20000.00'))
        self.assertEqual(totals['Mercado Pago'], Decimal('9800.00'))

    def test_physical_cash_balance_counts_only_cash_payments(self):
        cart = self._create_cart(Decimal('29800.00'))
        self._finalize(
            cart,
            [self.cash, self.mercado_pago],
            [Decimal('20000.00'), Decimal('9800.00')],
            [Decimal('25000.00'), None],
        )

        _, context = self._payment_method_totals_for(self.cash_register)
        request = self.factory.get('/')
        request.user = self.user

        self.assertEqual(context['efectivo_ingresos'], Decimal('20000.00'))
        self.assertEqual(context['balance_total'], Decimal('21000.00'))
        self.assertEqual(cash_register_amount(request)['actual_amount'], Decimal('21000.00'))
        self.assertEqual(self.cash_register.calculate_total(), Decimal('21000.00'))

    def test_sale_from_another_cash_register_is_excluded(self):
        cart = Cart.objects.create(
            user=self.user,
            company=self.company,
            is_completed=True,
            finalized_total=Decimal('9800.00'),
        )
        self.other_cash_register.carts.add(cart)
        CartPayment.objects.create(
            cart=cart,
            payment_method=self.mercado_pago,
            amount=Decimal('9800.00'),
        )

        totals, _ = self._payment_method_totals_for(self.cash_register)

        self.assertNotIn('Mercado Pago', totals)

    def test_sale_from_another_company_is_excluded_even_if_linked(self):
        cart = self._create_cart(
            Decimal('9800.00'),
            company=self.other_company,
        )
        CartPayment.objects.create(
            cart=cart,
            payment_method=self.mercado_pago,
            amount=Decimal('9800.00'),
        )
        cart.is_completed = True
        cart.finalized_total = Decimal('9800.00')
        cart.save()

        totals, _ = self._payment_method_totals_for(self.cash_register)

        self.assertNotIn('Mercado Pago', totals)

    def test_current_account_payment_creates_pending_debt_for_that_amount(self):
        cart = self._create_cart(Decimal('30000.00'))

        self._finalize(
            cart,
            [self.cash, self.current_account],
            [Decimal('10000.00'), Decimal('20000.00')],
            [Decimal('10000.00'), None],
            person=self.client,
        )

        pending_debt = Debt.objects.get(status='pendiente')
        paid_debt = Debt.objects.get(status='pagado')
        self.assertEqual(pending_debt.amount, Decimal('-20000.00'))
        self.assertEqual(paid_debt.amount, Decimal('10000.00'))
        self.assertEqual(self.client.total_debt(), Decimal('-20000.00'))

    def test_cart_is_not_counted_twice_when_it_has_multiple_lines(self):
        cart = Cart.objects.create(user=self.user, company=self.company)
        self.cash_register.carts.add(cart)
        CartLine.objects.create(
            cart=cart,
            item=None,
            quantity=Decimal('1.000'),
            price=Decimal('5000.00'),
            name='A',
            company=self.company,
        )
        CartLine.objects.create(
            cart=cart,
            item=None,
            quantity=Decimal('1.000'),
            price=Decimal('4800.00'),
            name='B',
            company=self.company,
        )

        self._finalize(
            cart,
            [self.mercado_pago],
            [Decimal('9800.00')],
        )
        totals, _ = self._payment_method_totals_for(self.cash_register)

        self.assertEqual(totals['Mercado Pago'], Decimal('9800.00'))


class CartPaymentMigrationTests(TransactionTestCase):
    migrate_from = [('checkout', '0011_cart_finalized_total')]
    migrate_to = [('checkout', '0012_cartpayment_migrate_historical_payments')]

    def setUp(self):
        super().setUp()
        self.watched_models = log_signals.WATCHED_MODELS
        log_signals.WATCHED_MODELS = []
        self.executor = MigrationExecutor(connection)
        self.executor.migrate(self.migrate_from)
        self.old_apps = self.executor.loader.project_state(
            self.migrate_from
        ).apps

    def tearDown(self):
        self.executor.loader.build_graph()
        self.executor.migrate(self.executor.loader.graph.leaf_nodes())
        log_signals.WATCHED_MODELS = self.watched_models
        super().tearDown()

    def _create_historical_cart(self, method_name, paid_amount=None, payment_return=None):
        Company = self.old_apps.get_model('users', 'Company')
        User = self.old_apps.get_model('auth', 'User')
        Cart = self.old_apps.get_model('checkout', 'Cart')
        CartLine = self.old_apps.get_model('checkout', 'CartLine')
        PaymentMethod = self.old_apps.get_model('checkout', 'PaymentMethod')

        company = Company.objects.create(name=f'{method_name} Company')
        user = User.objects.create(username=f'{method_name} user')
        payment_method = PaymentMethod.objects.create(name=method_name)
        cart = Cart.objects.create(
            user=user,
            company=company,
            payment_method=payment_method,
            paid_amount=paid_amount,
            payment_return=payment_return,
            finalized_total=Decimal('9800.00'),
            is_completed=True,
        )
        CartLine.objects.create(
            cart=cart,
            item=None,
            quantity=Decimal('1.000'),
            price=Decimal('9800.00'),
            name='Historical item',
            company=company,
        )
        return cart.pk

    def _migrate_and_get_payment(self, cart_id):
        self.executor.loader.build_graph()
        self.executor.migrate(self.migrate_to)
        new_apps = self.executor.loader.project_state(
            self.migrate_to
        ).apps
        CartPayment = new_apps.get_model('checkout', 'CartPayment')
        return CartPayment.objects.get(cart_id=cart_id)

    def test_migrates_historical_cash_sale(self):
        cart_id = self._create_historical_cart(
            'Efectivo',
            paid_amount=Decimal('10000.00'),
            payment_return=Decimal('200.00'),
        )

        payment = self._migrate_and_get_payment(cart_id)

        self.assertEqual(payment.amount, Decimal('9800.00'))
        self.assertEqual(payment.received_amount, Decimal('10000.00'))
        self.assertEqual(payment.change_amount, Decimal('200.00'))

    def test_migrates_historical_mercado_pago_sale(self):
        cart_id = self._create_historical_cart('Mercado Pago')

        payment = self._migrate_and_get_payment(cart_id)

        self.assertEqual(payment.amount, Decimal('9800.00'))
        self.assertIsNone(payment.received_amount)
        self.assertIsNone(payment.change_amount)
