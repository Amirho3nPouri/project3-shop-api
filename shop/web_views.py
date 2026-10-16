from django.shortcuts import render
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'shop/home.html'


class ProductListView(TemplateView):
    template_name = 'shop/product_list.html'


class ProductDetailView(TemplateView):
    template_name = 'shop/product_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slug'] = self.kwargs.get('slug')
        return context


class CategoryListView(TemplateView):
    template_name = 'shop/category_list.html'


class CartView(TemplateView):
    template_name = 'shop/cart.html'


class OrdersView(TemplateView):
    template_name = 'shop/orders.html'


class LoginView(TemplateView):
    template_name = 'shop/login.html'


class RegisterView(TemplateView):
    template_name = 'shop/register.html'


class ProfileView(TemplateView):
    template_name = 'shop/profile.html'


class NotFoundView(TemplateView):
    template_name = 'shop/404.html'


class ServerErrorView(TemplateView):
    template_name = 'shop/500.html'