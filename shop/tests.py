from django.test import TestCase
from django.contrib.auth.models import User
from decimal import Decimal

from .models import Category, Product, Cart, CartItem, Order, OrderItem
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse


class ProductAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="test12345")
        self.category = Category.objects.create(name="لباس", slug="lebas")
        self.product = Product.objects.create(
            category=self.category,
            name="تیشرت",
            slug="tshirt",
            price=Decimal("250000"),
            stock=10
        )

    def test_list_products_anonymous(self):
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_product_anonymous(self):
        url = reverse('product-list')
        data = {
            'category': self.category.id,
            'name': 'شلوار',
            'slug': 'shlvar',
            'price': 400000,
            'stock': 5,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_product_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('product-list')
        data = {
            'category': self.category.id,
            'name': 'شلوار',
            'slug': 'shlvar',
            'price': 400000,
            'stock': 5,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)

    def test_filter_products_by_category(self):
        url = reverse('product-list')
        response = self.client.get(url, {'category': self.category.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_products(self):
        url = reverse('product-list')
        response = self.client.get(url, {'search': 'تیشرت'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class RegisterAPITest(APITestCase):
    def test_register_user(self):
        url = reverse('register')
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'newpass12345',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="لباس", slug="lebas")

    def test_category_creation(self):
        self.assertEqual(self.category.name, "لباس")
        self.assertEqual(self.category.slug, "lebas")
        self.assertEqual(str(self.category), "لباس")

    def test_category_slug_unique(self):
        with self.assertRaises(Exception):
            Category.objects.create(name="لباس دوم", slug="lebas")


class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="لباس", slug="lebas")
        self.product = Product.objects.create(
            category=self.category,
            name="تیشرت",
            slug="tshirt",
            price=Decimal("250000"),
            stock=10
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, "تیشرت")
        self.assertEqual(self.product.price, Decimal("250000"))
        self.assertEqual(self.product.stock, 10)
        self.assertTrue(self.product.is_available)
        self.assertEqual(str(self.product), "تیشرت")

    def test_product_default_availability(self):
        self.assertTrue(self.product.is_available)

    def test_product_relation_with_category(self):
        self.assertEqual(self.product.category, self.category)
        self.assertIn(self.product, self.category.products.all())


class CartModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="test12345")
        self.cart = Cart.objects.create(user=self.user)
        self.category = Category.objects.create(name="لباس", slug="lebas")
        self.product = Product.objects.create(
            category=self.category,
            name="تیشرت",
            slug="tshirt",
            price=Decimal("250000"),
            stock=10
        )

    def test_cart_creation(self):
        self.assertEqual(self.cart.user, self.user)
        self.assertEqual(str(self.cart), f"سبد خرید {self.user.username}")

    def test_cart_total_price_empty(self):
        self.assertEqual(self.cart.total_price, 0)

    def test_cart_total_price_with_items(self):
        CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)
        self.assertEqual(self.cart.total_price, Decimal("500000"))


class CartItemModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="test12345")
        self.cart = Cart.objects.create(user=self.user)
        self.category = Category.objects.create(name="لباس", slug="lebas")
        self.product = Product.objects.create(
            category=self.category,
            name="تیشرت",
            slug="tshirt",
            price=Decimal("250000"),
            stock=10
        )

    def test_cart_item_creation(self):
        item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=3)
        self.assertEqual(item.quantity, 3)
        self.assertEqual(item.subtotal, Decimal("750000"))
        self.assertEqual(str(item), "3 x تیشرت")


class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="test12345")
        self.order = Order.objects.create(user=self.user)

    def test_order_creation(self):
        self.assertEqual(self.order.user, self.user)
        self.assertEqual(self.order.status, "pending")
        self.assertEqual(self.order.total_price, 0)

    def test_order_str(self):
        self.assertIn("testuser", str(self.order))