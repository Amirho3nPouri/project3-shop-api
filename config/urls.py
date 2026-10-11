from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)


def home(request):
    return JsonResponse({
        'message': 'به API فروشگاه امیر خوش آمدید! 🛒',
        'endpoints': {
            'docs (swagger)': '/api/docs/',
            'docs (redoc)': '/api/redoc/',
            'schema': '/api/schema/',
            'products': '/api/products/',
            'categories': '/api/categories/',
            'cart': '/api/cart/',
            'orders': '/api/orders/',
            'register': '/api/register/',
            'admin': '/admin/',
        }
    })


urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('api/', include('shop.urls')),

    # مستندات API
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)