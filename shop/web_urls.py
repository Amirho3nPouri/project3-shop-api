from django.urls import path
from . import web_views

app_name = 'web'

urlpatterns = [
    path('', web_views.HomeView.as_view(), name='home'),
    path('products/', web_views.ProductListView.as_view(), name='product_list'),
    path('products/<slug:slug>/', web_views.ProductDetailView.as_view(), name='product_detail'),
    path('categories/', web_views.CategoryListView.as_view(), name='category_list'),
    path('cart/', web_views.CartView.as_view(), name='cart'),
    path('orders/', web_views.OrdersView.as_view(), name='orders'),
    path('login/', web_views.LoginView.as_view(), name='login'),
    path('register/', web_views.RegisterView.as_view(), name='register'),
    path('profile/', web_views.ProfileView.as_view(), name='profile'),
    path('404/', web_views.NotFoundView.as_view(), name='not_found'),
    path('500/', web_views.ServerErrorView.as_view(), name='server_error'),
    path('about/', web_views.AboutView.as_view(), name='about'),
    path('contact/', web_views.ContactView.as_view(), name='contact'),
    path('faq/', web_views.FAQView.as_view(), name='faq'),               # ← جدید
    path('shipping/', web_views.ShippingView.as_view(), name='shipping'),  # ← جدید
    path('privacy/', web_views.PrivacyView.as_view(), name='privacy'),   # ← جدید
]