from decimal import Decimal
from django.test import RequestFactory, TestCase
from django.urls import reverse

from catalog.models import Category, Product
from cart.cart import Cart


class CartTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.category = Category.objects.create(name='Cookies', slug='cookies')
        self.product1 = Product.objects.create(
            category=self.category,
            name='Choc Chip Cookie',
            slug='choc-chip-cookie',
            price='3.50',
            stock=15,
            available=True,
        )
        self.product2 = Product.objects.create(
            category=self.category,
            name='Anzac Biscuit',
            slug='anzac-biscuit',
            price='4.00',
            stock=10,
            available=True,
        )

    def test_cart_session_operations(self):
        session = self.client.session
        cart = Cart(self.client)

        cart.add(self.product1, quantity=2)
        self.assertEqual(len(cart), 2)
        self.assertEqual(cart.get_total_price(), Decimal('7.00'))

        # Add more of same product
        cart.add(self.product1, quantity=1)
        self.assertEqual(len(cart), 3)
        self.assertEqual(cart.get_total_price(), Decimal('10.50'))

        # Override quantity
        cart.add(self.product1, quantity=1, update_quantity=True)
        self.assertEqual(len(cart), 1)

        # Add second product
        cart.add(self.product2, quantity=2)
        self.assertEqual(len(cart), 3)
        self.assertEqual(cart.get_total_price(), Decimal('11.50'))

        # Remove product
        cart.remove(self.product1)
        self.assertEqual(len(cart), 2)
        self.assertEqual(cart.get_total_price(), Decimal('8.00'))

        # Clear cart
        cart.clear()
        self.assertEqual(len(cart), 0)

    def test_cart_views(self):
        # 1. View cart detail
        response = self.client.get(reverse('cart:cart_detail'))
        self.assertEqual(response.status_code, 200)

        # 2. Add product via POST
        response = self.client.post(
            reverse('cart:cart_add', args=[self.product1.id]),
            {'quantity': 2, 'override': False}
        )
        self.assertRedirects(response, reverse('cart:cart_detail'))

        # 3. Remove product via POST
        response = self.client.post(reverse('cart:cart_remove', args=[self.product1.id]))
        self.assertRedirects(response, reverse('cart:cart_detail'))
