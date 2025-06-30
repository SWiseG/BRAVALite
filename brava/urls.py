from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API REST endpoints
    path('api/v1/auth/', include('users.urls')),
    path('api/v1/dashboard/', include('dashboard.urls')),
    path('api/v1/products/', include('products.urls')),
    path('api/v1/orders/', include('orders.urls')),
    path('api/v1/customers/', include('customers.urls')),
    path('api/v1/core/', include('core.urls')),
    
    # SPA - Single entry point
    path('', TemplateView.as_view(template_name='Index.html'), name='web'),
]

# Media and static files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Catch-all pattern para SPA routing
urlpatterns += [
    path('<path:path>', TemplateView.as_view(template_name='Index.html')),
]
