"""
Script to generate all backend view and URL files
Run this with: python generate_backend_files.py
"""

PRODUCTS_VIEWS = """from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Product, ProductVideo
from .serializers import CategorySerializer, ProductListSerializer, ProductDetailSerializer, ProductVideoSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(is_active=True).select_related('category').prefetch_related('images', 'videos')
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category__slug', 'price']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at', 'name']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductListSerializer

    @action(detail=True, methods=['get'])
    def videos(self, request, slug=None):
        product = self.get_object()
        videos = product.videos.all()
        serializer = ProductVideoSerializer(videos, many=True, context={'request': request})
        return Response(serializer.data)
"""

CART_VIEWS = """from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from products.models import Product


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Cart.objects.filter(user=self.request.user)
        else:
            session_key = self.request.session.session_key
            if not session_key:
                self.request.session.create()
                session_key = self.request.session.session_key
            return Cart.objects.filter(session_key=session_key)

    def get_cart(self):
        if self.request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=self.request.user)
        else:
            session_key = self.request.session.session_key
            if not session_key:
                self.request.session.create()
                session_key = self.request.session.session_key
            cart, created = Cart.objects.get_or_create(session_key=session_key)
        return cart

    def list(self, request):
        cart = self.get_cart()
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def add_item(self, request):
        cart = self.get_cart()
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        try:
            product = Product.objects.get(id=product_id, is_active=True)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += int(quantity)
        else:
            cart_item.quantity = int(quantity)
        cart_item.save()

        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['patch'])
    def update_item(self, request):
        cart = self.get_cart()
        item_id = request.data.get('item_id')
        quantity = request.data.get('quantity')

        try:
            cart_item = CartItem.objects.get(id=item_id, cart=cart)
            cart_item.quantity = int(quantity)
            cart_item.save()
            serializer = CartSerializer(cart)
            return Response(serializer.data)
        except CartItem.DoesNotExist:
            return Response({'error': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['delete'])
    def remove_item(self, request):
        cart = self.get_cart()
        item_id = request.query_params.get('item_id')

        try:
            cart_item = CartItem.objects.get(id=item_id, cart=cart)
            cart_item.delete()
            serializer = CartSerializer(cart)
            return Response(serializer.data)
        except CartItem.DoesNotExist:
            return Response({'error': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['delete'])
    def clear(self, request):
        cart = self.get_cart()
        cart.items.all().delete()
        serializer = CartSerializer(cart)
        return Response(serializer.data)
"""

ORDERS_VIEWS = """from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import stripe
import json
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderCreateSerializer
from cart.models import Cart

stripe.api_key = settings.STRIPE_SECRET_KEY


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items')

    @action(detail=False, methods=['post'])
    def create_payment_intent(self, request):
        try:
            if request.user.is_authenticated:
                cart = Cart.objects.get(user=request.user)
            else:
                return Response({'error': 'Must be authenticated to checkout'}, status=status.HTTP_401_UNAUTHORIZED)

            if not cart.items.exists():
                return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

            amount = int(cart.total_price * 100)  # Convert to cents

            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency='usd',
                metadata={'user_id': request.user.id}
            )

            return Response({
                'client_secret': intent.client_secret,
                'amount': cart.total_price
            })

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def confirm_order(self, request):
        try:
            payment_intent_id = request.data.get('payment_intent_id')
            address_data = request.data

            # Verify payment intent
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            if intent.status != 'succeeded':
                return Response({'error': 'Payment not completed'}, status=status.HTTP_400_BAD_REQUEST)

            cart = Cart.objects.get(user=request.user)

            # Create order
            order = Order.objects.create(
                user=request.user,
                total_amount=cart.total_price,
                stripe_payment_intent_id=payment_intent_id,
                shipping_address_line1=address_data.get('shipping_address_line1'),
                shipping_address_line2=address_data.get('shipping_address_line2', ''),
                shipping_city=address_data.get('shipping_city'),
                shipping_state=address_data.get('shipping_state'),
                shipping_postal_code=address_data.get('shipping_postal_code'),
                shipping_country=address_data.get('shipping_country', 'US'),
                billing_address_line1=address_data.get('billing_address_line1'),
                billing_address_line2=address_data.get('billing_address_line2', ''),
                billing_city=address_data.get('billing_city'),
                billing_state=address_data.get('billing_state'),
                billing_postal_code=address_data.get('billing_postal_code'),
                billing_country=address_data.get('billing_country', 'US'),
                status='processing'
            )

            # Create order items from cart
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity
                )

            # Clear cart
            cart.items.all().delete()

            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
@permission_classes([])
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        # Handle successful payment
        pass

    return HttpResponse(status=200)
"""

RATINGS_VIEWS = """from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import ProductRating
from .serializers import ProductRatingSerializer
from products.models import Product


class ProductRatingViewSet(viewsets.ModelViewSet):
    serializer_class = ProductRatingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        product_slug = self.kwargs.get('product_slug')
        if product_slug:
            return ProductRating.objects.filter(product__slug=product_slug)
        return ProductRating.objects.all()

    def perform_create(self, serializer):
        product_slug = self.kwargs.get('product_slug')
        product = get_object_or_404(Product, slug=product_slug)
        serializer.save(user=self.request.user, product=product)

    def create(self, request, *args, **kwargs):
        product_slug = self.kwargs.get('product_slug')
        product = get_object_or_404(Product, slug=product_slug)

        # Check if user already rated this product
        existing_rating = ProductRating.objects.filter(user=request.user, product=product).first()
        if existing_rating:
            # Update existing rating
            serializer = self.get_serializer(existing_rating, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return super().create(request, *args, **kwargs)
"""

COMMENTS_VIEWS = """from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from .models import ProductComment
from .serializers import ProductCommentSerializer
from products.models import Product


class ProductCommentViewSet(viewsets.ModelViewSet):
    serializer_class = ProductCommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        product_slug = self.kwargs.get('product_slug')
        if product_slug:
            return ProductComment.objects.filter(product__slug=product_slug, parent_comment=None).prefetch_related('replies')
        return ProductComment.objects.filter(parent_comment=None)

    def perform_create(self, serializer):
        product_slug = self.kwargs.get('product_slug')
        product = get_object_or_404(Product, slug=product_slug)
        serializer.save(user=self.request.user, product=product)
"""

# Write all views files
with open('products/views.py', 'w') as f:
    f.write(PRODUCTS_VIEWS)

with open('cart/views.py', 'w') as f:
    f.write(CART_VIEWS)

with open('orders/views.py', 'w') as f:
    f.write(ORDERS_VIEWS)

with open('ratings/views.py', 'w') as f:
    f.write(RATINGS_VIEWS)

with open('comments/views.py', 'w') as f:
    f.write(COMMENTS_VIEWS)

print("All view files generated successfully!")
