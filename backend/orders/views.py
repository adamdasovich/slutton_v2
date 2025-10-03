from rest_framework import viewsets, status
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
