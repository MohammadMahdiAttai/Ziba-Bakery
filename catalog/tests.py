from django.test import TestCase
from django.urls import reverse

from .models import Category, Product


class CatalogModelAndViewsTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Cupcakes', slug='cupcakes', icon='🧁')
        self.product = Product.objects.create(
            category=self.category,
            name='Chocolate Cupcake',
            slug='chocolate-cupcake',
            description='Rich and delicious',
            price='5.50',
            stock=10,
            available=True,
        )

    def test_category_model(self):
        self.assertEqual(str(self.category), 'Cupcakes')
        self.assertEqual(self.category.get_absolute_url(), reverse('catalog:product_list_by_category', args=['cupcakes']))

    def test_product_model(self):
        self.assertEqual(str(self.product), 'Chocolate Cupcake')
        self.assertEqual(
            self.product.get_absolute_url(),
            reverse('catalog:product_detail', args=[self.product.id, self.product.slug])
        )
        self.assertTrue(self.product.in_stock())

        self.product.stock = 0
        self.assertFalse(self.product.in_stock())

    def test_product_list_view(self):
        response = self.client.get(reverse('catalog:product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/product_list.html')
        self.assertIn('products', response.context)
        self.assertEqual(len(response.context['products']), 1)

    def test_product_list_by_category_view(self):
        response = self.client.get(reverse('catalog:product_list_by_category', args=['cupcakes']))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['category'], self.category)

    def test_product_detail_view(self):
        response = self.client.get(self.product.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/product_detail.html')
        self.assertEqual(response.context['product'], self.product)

    def test_product_detail_not_found(self):
        response = self.client.get(reverse('catalog:product_detail', args=[9999, 'non-existent']))
        self.assertEqual(response.status_code, 404)
