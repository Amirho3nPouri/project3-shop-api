from django.contrib.auth.models import User

from rest_framework import viewsets, permissions, status, generics, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.throttling import AnonRateThrottle

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, inline_serializer

from .models import Category, Product, Cart, CartItem, Order, OrderItem
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    CartSerializer,
    CartItemSerializer,
    OrderSerializer,
    OrderItemSerializer,
    UserProfileSerializer,
    RegisterSerializer,
    ChangePasswordSerializer,
)

import logging
logger = logging.getLogger('shop')

# ==================== Category ====================

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


# ==================== Product ====================

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'   # ← این خط

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'is_available']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at', 'name', 'stock']
    ordering = ['-created_at']

# ==================== Cart ====================

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def get_or_create_cart(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart

    @extend_schema(
        responses={200: CartSerializer},
        description='سبد خرید کاربر لاگین‌شده رو برمی‌گردونه.'
    )
    @action(detail=False, methods=['get'])
    def my_cart(self, request):
        cart = self.get_or_create_cart()
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    @extend_schema(
        request=None,
        responses={200: None},
        description='کل سبد خرید رو خالی می‌کنه.'
    )
    @action(detail=False, methods=['post'])
    def clear(self, request):
        cart = self.get_or_create_cart()
        cart.items.all().delete()
        return Response(
            {'message': 'سبد خرید خالی شد. ✅'},
            status=status.HTTP_200_OK
        )

    @extend_schema(
        request=inline_serializer(
            name='CartAddRequest',
            fields={
                'product_id': serializers.IntegerField(help_text='ID محصول'),
                'quantity': serializers.IntegerField(default=1, help_text='تعداد'),
            }
        ),
        responses={200: CartSerializer, 400: None, 404: None},
        description='یه محصول به سبد خرید اضافه می‌کنه. اگه محصول قبلاً تو سبد باشه، تعدادش جمع می‌شه.'
    )
    @action(detail=False, methods=['post'])
    def add(self, request):
        cart = self.get_or_create_cart()
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        if not product_id:
            return Response(
                {'error': 'product_id لازمه.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if quantity < 1:
            return Response(
                {'error': 'تعداد باید حداقل ۱ باشه.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {'error': 'محصول پیدا نشد.'},
                status=status.HTTP_404_NOT_FOUND
            )

        if not product.is_available:
            return Response(
                {'error': 'این محصول در حال حاضر موجود نیست.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        existing_item = CartItem.objects.filter(cart=cart, product=product).first()
        if existing_item:
            new_quantity = existing_item.quantity + quantity
            if new_quantity > product.stock:
                return Response(
                    {'error': f'حداکثر موجودی این محصول {product.stock} عدد است. '
                              f'شما در حال حاضر {existing_item.quantity} عدد در سبد دارید.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            existing_item.quantity = new_quantity
            existing_item.save()
        else:
            if quantity > product.stock:
                return Response(
                    {'error': f'حداکثر موجودی این محصول {product.stock} عدد است.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            CartItem.objects.create(cart=cart, product=product, quantity=quantity)

        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)


# ==================== CartItem ====================

class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product']

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)

    def perform_create(self, serializer):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        product = serializer.validated_data['product']
        quantity = serializer.validated_data.get('quantity', 1)

        existing_item = CartItem.objects.filter(cart=cart, product=product).first()
        if existing_item:
            new_quantity = existing_item.quantity + quantity
            if new_quantity > product.stock:
                raise serializers.ValidationError(
                    {'quantity': f'حداکثر موجودی این محصول {product.stock} عدد است. '
                                 f'شما در حال حاضر {existing_item.quantity} عدد در سبد دارید.'}
                )
            existing_item.quantity = new_quantity
            existing_item.save()
            serializer.instance = existing_item
        else:
            serializer.save(cart=cart)


# ==================== Order ====================

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status']
    ordering_fields = ['created_at', 'total_price']
    ordering = ['-created_at']

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    @extend_schema(
        request=None,
        responses={201: OrderSerializer, 400: None},
        description='سبد خرید فعلی رو به یه سفارش تبدیل می‌کنه و سبد رو خالی می‌کنه.'
    )
    @action(detail=False, methods=['post'])
    def checkout(self, request):
        cart = Cart.objects.filter(user=request.user).first()
        if not cart or not cart.items.exists():
            return Response(
                {'error': 'سبد خرید خالیه!'},
                status=status.HTTP_400_BAD_REQUEST
            )

        order = Order.objects.create(
            user=request.user,
            total_price=cart.total_price
        )
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                product_name=item.product.name,
                price=item.product.price,
                quantity=item.quantity
            )
        cart.items.all().delete()
        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# ==================== Auth ====================

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    throttle_classes = [AnonRateThrottle]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # تولید JWT برای کاربر جدید
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                'message': 'ثبت‌نام با موفقیت انجام شد. ✅',
                'user': UserProfileSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                },
            },
            status=status.HTTP_201_CREATED
        )


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {'message': 'رمز عبور با موفقیت تغییر کرد. ✅'},
            status=status.HTTP_200_OK
        )