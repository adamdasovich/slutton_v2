from rest_framework import viewsets
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
