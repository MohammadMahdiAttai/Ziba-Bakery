from decimal import Decimal
from django.test import TestCase
from django.urls import reverse

from catalog.models import Category, Product
from orders.forms import _luhn_is_valid, PaymentForm
from orders.models import Order, OrderItem


class OrdersTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Cakes', slug='cakes')
        self.product = Product.objects.create(
            category=self.category,
            name='Mud Cake',
            slug='mud-cake',
            price='50.00',
            stock=5,
            available=True,
        )

    def test_luhn_algorithm(self):
        self.assertTrue(_luhn_is_valid('4242424242424242'))
        self.assertFalse(_luhn_is_valid('4242424242424241'))

    def test_payment_form(self):
        # Valid form
        form = PaymentForm(data={
            'card_number': '4242 4242 4242 4242',
            'expiry': '12/29',
            'cvc': '123'
        })
        self.assertTrue(form.is_valid())

        # Invalid card number (fails Luhn)
        form_invalid_card = PaymentForm(data={
            'card_number': '4242 4242 4242 4241',
            'expiry': '12/29',
            'cvc': '123'
        })
        self.assertFalse(form_invalid_card.is_valid())

        # Expired card
        form_expired = PaymentForm(data={
            'card_number': '4242 4242 4242 4242',
            'expiry': '01/20',
            'cvc': '123'
        })
        self.assertFalse(form_expired.is_valid())

    def test_order_model(self):
        order = Order.objects.create(
            first_name='John',
            last_name='Smith',
            email='john@example.com',
            address='100 Collins St',
            suburb='Melbourne',
            postcode='3000',
            paid=True,
        )
        item = OrderItem.objects.create(
            order=order,
            product=self.product,
            price=Decimal('50.00'),
            quantity=2,
        )
        self.assertEqual(item.get_cost(), Decimal('100.00'))
        self.assertEqual(order.get_total_cost(), Decimal('100.00'))
        self.assertEqual(str(order), f'Order #{order.id}')

    def test_checkout_pipeline(self):
        # 1. Order create when cart is empty -> redirects to shop
        response = self.client.get(reverse('orders:order_create'))
        self.assertRedirects(response, reverse('catalog:product_list'))

        # 2. Add product to cart
        self.client.post(
            reverse('cart:cart_add', args=[self.product.id]),
            {'quantity': 2, 'override': False}
        )

        # 3. Order create GET with items in cart -> status 200
        response = self.client.get(reverse('orders:order_create'))
        self.assertEqual(response.status_code, 200)

        # 4. Order create POST with delivery details
        delivery_data = {
            'first_name': 'Sarah',
            'last_name': 'Connor',
            'email': 'sarah@example.com',
            'address': '456 Queen St',
            'suburb': 'Melbourne',
            'postcode': '3000'
        }
        response = self.client.post(reverse('orders:order_create'), delivery_data)
        self.assertRedirects(response, reverse('orders:order_payment'))

        # 5. Payment POST with valid demo card
        payment_data = {
            'card_number': '4242 4242 4242 4242',
            'expiry': '12/29',
            'cvc': '999'
        }
        response = self.client.post(reverse('orders:order_payment'), payment_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/created.html')

        # Check order created
        order = Order.objects.get(email='sarah@example.com')
        self.assertTrue(order.paid)
        self.assertEqual(order.items.count(), 1)

        # Check stock deducted (5 - 2 = 3)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 3)

        # Check cart cleared
        cart_response = self.client.get(reverse('cart:cart_detail'))
        self.assertEqual(len(cart_response.context['cart']), 0)
