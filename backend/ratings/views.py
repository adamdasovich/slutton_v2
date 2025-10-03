from rest_framework import viewsets, status
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
