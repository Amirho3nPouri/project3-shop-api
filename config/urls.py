from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns   # ← این خط
from django.http import JsonResponse

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

from django.contrib.auth import views as auth_views


# ==================== Error Handlers ====================

def custom_404(request, exception):
    return JsonResponse({
        'error': 'Not Found',
        'status_code': 404,
        'message': 'آدرسی که خواستی وجود نداره.',
        'path': request.path,
    }, status=404, json_dumps_params={'ensure_ascii': False, 'indent': 2})


from django.shortcuts import render


def custom_500(request):
    # اگه درخواست به /api/ بود، JSON برگردون
    if request.path.startswith('/api/'):
        return JsonResponse({
            'error': 'Internal Server Error',
            'status_code': 500,
            'message': 'خطای غیرمنتظره‌ای رخ داد. لطفاً بعداً تلاش کن.',
        }, status=500, json_dumps_params={'ensure_ascii': False, 'indent': 2})
    # وگرنه HTML
    return render(request, 'shop/500.html', status=500)


# ==================== URL Patterns ====================

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # API (JSON)
    path('api/', include('shop.urls')),

    # JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # مستندات
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # Password Reset
    path('api/password-reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html',
        email_template_name='registration/password_reset_email.html',
        subject_template_name='registration/password_reset_subject.txt',
        success_url='/api/password-reset/done/',
        from_email='noreply@amirshop.ir',
    ), name='password_reset'),

    path('api/password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html',
    ), name='password_reset_done'),

    path('api/password-reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html',
        success_url='/api/password-reset/complete/',
    ), name='password_reset_confirm'),

    path('api/password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html',
    ), name='password_reset_complete'),

    # Frontend (HTML)
    path('', include('shop.web_urls')),
]


# ==================== Static & Media ====================

urlpatterns += staticfiles_urlpatterns()   # ← این خط (برای استاتیک)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# ==================== Error Handlers ====================

handler404 = 'config.urls.custom_404'
handler500 = 'config.urls.custom_500'

# قبل
def custom_404(request, exception):
    return JsonResponse({...}, status=404)


# بعد
from django.shortcuts import render

def custom_404(request, exception):
    return render(request, 'shop/404.html', status=404)

def custom_404(request, exception):
    # اگه درخواست به /api/ بود، JSON برگردون
    if request.path.startswith('/api/'):
        return JsonResponse({
            'error': 'Not Found',
            'status_code': 404,
            'message': 'آدرسی که خواستی وجود نداره.',
        }, status=404, json_dumps_params={'ensure_ascii': False, 'indent': 2})
    # وگرنه HTML
    return render(request, 'shop/404.html', status=404)