from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from decimal import Decimal

from .models import Category, Product, Cart, CartItem, Order, OrderItem


# ==================== Model Tests ====================

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
            category=self.category, name="تیشرت", slug="tshirt",
            price=Decimal("250000"), stock=10
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, "تیشرت")
        self.assertEqual(self.product.price, Decimal("250000"))
        self.assertEqual(self.product.stock, 10)
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
            category=self.category, name="تیشرت", slug="tshirt",
            price=Decimal("250000"), stock=10
        )

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
            category=self.category, name="تیشرت", slug="tshirt",
            price=Decimal("250000"), stock=10
        )

    def test_cart_item_subtotal(self):
        item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=3)
        self.assertEqual(item.quantity, 3)
        self.assertEqual(item.subtotal, Decimal("750000"))


class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="test12345")
        self.order = Order.objects.create(user=self.user)

    def test_order_default_status(self):
        self.assertEqual(self.order.status, "pending")

    def test_order_str(self):
        self.assertIn("testuser", str(self.order))


# ==================== Auth Tests ====================

class RegisterAPITest(APITestCase):
    def test_register_user_with_tokens(self):
        url = reverse('register')
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'newpass12345',
            'password_confirm': 'newpass12345',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('tokens', response.data)
        self.assertIn('access', response.data['tokens'])
        self.assertIn('refresh', response.data['tokens'])
        self.assertEqual(User.objects.count(), 1)

    def test_register_password_mismatch(self):
        url = reverse('register')
        data = {
            'username': 'newuser',
            'password': 'newpass12345',
            'password_confirm': 'different12345',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_duplicate_username(self):
        User.objects.create_user(username='exists', password='test12345')
        url = reverse('register')
        data = {
            'username': 'exists',
            'password': 'newpass12345',
            'password_confirm': 'newpass12345',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class JWTAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="test12345")

    def test_obtain_token(self):
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {
            'username': 'testuser',
            'password': 'test12345',
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_obtain_token_wrong_password(self):
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {
            'username': 'testuser',
            'password': 'wrongpass',
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ProfileAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="test12345", email="test@example.com"
        )
        self.client.force_authenticate(user=self.user)

    def test_get_profile(self):
        url = reverse('profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['email'], 'test@example.com')

    def test_update_profile(self):
        url = reverse('profile')
        response = self.client.patch(url, {
            'first_name': 'امیر',
            'last_name': 'پوری',
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'امیر')

    def test_change_password(self):
        url = reverse('change-password')
        response = self.client.put(url, {
            'old_password': 'test12345',
            'new_password': 'newpass12345',
            'new_password_confirm': 'newpass12345',
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpass12345'))

    def test_change_password_wrong_old(self):
        url = reverse('change-password')
        response = self.client.put(url, {
            'old_password': 'wrongpass',
            'new_password': 'newpass12345',
            'new_password_confirm': 'newpass12345',
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# ==================== Product Tests ====================

class ProductAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="test12345")
        self.category = Category.objects.create(name="لباس", slug="lebas")
        self.product = Product.objects.create(
            category=self.category, name="تیشرت", slug="tshirt",
            price=Decimal("250000"), stock=10
        )

    def test_list_products_anonymous(self):
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_product_anonymous(self):
        url = reverse('product-list')
        response = self.client.post(url, {
            'category': self.category.id,
            'name': 'شلوار', 'slug': 'shlvar',
            'price': 400000, 'stock': 5,
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_product_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('product-list')
        response = self.client.post(url, {
            'category': self.category.id,
            'name': 'شلوار', 'slug': 'shlvar',
            'price': 400000, 'stock': 5,
        })
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


# ==================== Cart Tests ====================

class CartAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="test12345")
        self.category = Category.objects.create(name="لباس", slug="lebas")
        self.product = Product.objects.create(
            category=self.category, name="تیشرت", slug="tshirt",
            price=Decimal("250000"), stock=10
        )
        self.client.force_authenticate(user=self.user)

    def test_my_cart_empty(self):
        url = reverse('cart-my-cart')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_items'], 0)
        self.assertEqual(Decimal(response.data['total_price']), Decimal('0'))
    def test_add_to_cart(self):
        url = reverse('cart-add')
        response = self.client.post(url, {
            'product_id': self.product.id,
            'quantity': 2,
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_items'], 2)

    def test_add_to_cart_exceeds_stock(self):
        url = reverse('cart-add')
        response = self.client.post(url, {
            'product_id': self.product.id,
            'quantity': 20,
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_same_product_merges_quantity(self):
        url = reverse('cart-add')
        self.client.post(url, {'product_id': self.product.id, 'quantity': 2})
        response = self.client.post(url, {'product_id': self.product.id, 'quantity': 3})
        self.assertEqual(response.data['total_items'], 5)

    def test_clear_cart(self):
        url = reverse('cart-add')
        self.client.post(url, {'product_id': self.product.id, 'quantity': 2})
        clear_url = reverse('cart-clear')
        response = self.client.post(clear_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(CartItem.objects.count(), 0)


# ==================== Order Tests ====================

class OrderAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="test12345")
        self.category = Category.objects.create(name="لباس", slug="lebas")
        self.product = Product.objects.create(
            category=self.category, name="تیشرت", slug="tshirt",
            price=Decimal("250000"), stock=10
        )
        self.client.force_authenticate(user=self.user)

    def test_checkout_empty_cart(self):
        url = reverse('orders-checkout')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_checkout_success(self):
        add_url = reverse('cart-add')
        self.client.post(add_url, {'product_id': self.product.id, 'quantity': 2})

        url = reverse('orders-checkout')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderItem.objects.count(), 1)
        self.assertEqual(CartItem.objects.count(), 0)

        order = Order.objects.first()
        self.assertEqual(order.total_price, Decimal("500000"))