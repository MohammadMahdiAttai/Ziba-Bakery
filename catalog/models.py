from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True,
                             help_text='Used in the URL, e.g. "cupcakes"')
    icon = models.CharField(max_length=10, default='🍰',
                             help_text='Emoji shown when a product has no photo')

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog:product_list_by_category', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products',
                                  on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2,
                                 help_text='Price in AUD, e.g. 24.95')
    image = models.ImageField(upload_to='products/%Y/%m/', blank=True)
    available = models.BooleanField(default=True,
                                     help_text='Untick to hide this product from the shop')
    stock = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        indexes = [models.Index(fields=['id', 'slug'])]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog:product_detail', args=[self.id, self.slug])

    def in_stock(self):
        return self.available and self.stock > 0
