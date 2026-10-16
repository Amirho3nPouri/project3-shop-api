from django.contrib.auth.models import User
from django.db.models import Sum
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Category, Product, Cart, CartItem, Order, OrderItem

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

# ==================== User & Auth ====================

class UserProfileSerializer(serializers.ModelSerializer):
    total_orders = serializers.SerializerMethodField()
    total_spent = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'date_joined', 'last_login', 'total_orders', 'total_spent'
        ]
        read_only_fields = ['id', 'username', 'date_joined', 'last_login']

    def get_total_orders(self, obj):
        return obj.orders.count()

    def get_total_spent(self, obj):
        total = obj.orders.filter(status='paid').aggregate(
            total=Sum('total_price')
        )['total'] or 0
        return total


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True, max_length=150)
    last_name = serializers.CharField(required=False, allow_blank=True, max_length=150)
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'password', 'password_confirm'
        ]
        read_only_fields = ['id']

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('این نام کاربری قبلاً گرفته شده.')
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('این ایمیل قبلاً ثبت شده.')
        return value

    def validate_password(self, value):
        """اعتبارسنجی رمز عبور با قوانین جنگو"""
        try:
            validate_password(value)
        except ValidationError as e:
            # ترجمه‌ی پیام‌های خطا به فارسی
            persian_messages = []
            for msg in e.messages:
                msg_lower = msg.lower()
                if 'too short' in msg_lower:
                    persian_messages.append('رمز عبور باید حداقل ۸ کاراکتر باشه.')
                elif 'too common' in msg_lower:
                    persian_messages.append('این رمز خیلی رایجه. یه رمز قوی‌تر انتخاب کن.')
                elif 'entirely numeric' in msg_lower:
                    persian_messages.append('رمز عبور نباید کاملاً عددی باشه. ترکیب حرف و عدد استفاده کن.')
                elif 'too similar' in msg_lower:
                    persian_messages.append('رمز عبور نباید شبیه اطلاعات شخصیت باشه.')
                else:
                    persian_messages.append(msg)
            raise serializers.ValidationError(persian_messages)
        return value

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError(
                {'password_confirm': 'رمزهای عبور یکسان نیستن.'}
            )
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data.get('last_name', ''),
        )
        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True, min_length=8)
    new_password_confirm = serializers.CharField(required=True, write_only=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('رمز عبور فعلی اشتباهه.')
        return value

    def validate(self, data):
        if data['new_password'] != data['new_password_confirm']:
            raise serializers.ValidationError(
                {'new_password_confirm': 'رمزهای جدید یکسان نیستن.'}
            )
        return data

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


# ==================== Category ====================

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'created_at']
        read_only_fields = ['id', 'created_at']


# ==================== Product ====================

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'category', 'category_name', 'name', 'slug',
            'description', 'price', 'stock', 'image',
            'is_available', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


# ==================== Cart ====================

class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_slug = serializers.CharField(source='product.slug', read_only=True)
    product_price = serializers.DecimalField(
        source='product.price', max_digits=10, decimal_places=0, read_only=True
    )
    subtotal = serializers.DecimalField(max_digits=12, decimal_places=0, read_only=True)

    class Meta:
        model = CartItem
        fields = [
            'id', 'product', 'product_name', 'product_slug',
            'product_price', 'quantity', 'subtotal', 'added_at'
        ]
        read_only_fields = ['id', 'added_at']

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("تعداد باید حداقل ۱ باشه.")
        return value

    def validate(self, data):
        product = data.get('product') or (self.instance.product if self.instance else None)
        quantity = data.get('quantity', 1)

        if product and not product.is_available:
            raise serializers.ValidationError(
                {'product': 'این محصول در حال حاضر موجود نیست.'}
            )

        if product and quantity > product.stock:
            raise serializers.ValidationError(
                {'quantity': f'حداکثر موجودی این محصول {product.stock} عدد است.'}
            )

        return data


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(max_digits=12, decimal_places=0, read_only=True)
    total_items = serializers.SerializerMethodField()
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Cart
        fields = [
            'id', 'user', 'user_username', 'items',
            'total_items', 'total_price', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def get_total_items(self, obj):
        return sum(item.quantity for item in obj.items.all())


# ==================== Order ====================

class OrderItemSerializer(serializers.ModelSerializer):
    subtotal = serializers.DecimalField(max_digits=12, decimal_places=0, read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'price', 'quantity', 'subtotal']
        read_only_fields = ['id']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'user_username', 'status',
            'total_price', 'items', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'total_price', 'created_at', 'updated_at']