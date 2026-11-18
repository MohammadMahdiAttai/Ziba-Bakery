from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = 'Ziba Bakery Administration'
admin.site.site_title = 'Ziba Bakery Admin'
admin.site.index_title = 'Manage products, orders and customers'

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('core.urls')),
    path('shop/', include('catalog.urls')),
    path('accounts/', include('accounts.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
