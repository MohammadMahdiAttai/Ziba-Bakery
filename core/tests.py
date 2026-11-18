from django.core import mail
from django.test import TestCase
from django.urls import reverse

from catalog.models import Category, Product


class CoreViewsTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category', slug='test-cat')
        self.product = Product.objects.create(
            category=self.category,
            name='Test Pastry',
            slug='test-pastry',
            price='10.00',
            stock=5,
            available=True,
        )

    def test_home_page(self):
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/home.html')
        self.assertIn('featured_products', response.context)
        self.assertEqual(len(response.context['featured_products']), 1)

    def test_about_page(self):
        response = self.client.get(reverse('core:about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/about.html')

    def test_contact_page_get(self):
        response = self.client.get(reverse('core:contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/contact.html')

    def test_contact_page_post_valid(self):
        data = {
            'name': 'Jane Doe',
            'email': 'jane@example.com',
            'message': 'Love your pastries!',
        }
        response = self.client.post(reverse('core:contact'), data)
        self.assertRedirects(response, reverse('core:contact'))
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Ziba Bakery enquiry', mail.outbox[0].subject)
