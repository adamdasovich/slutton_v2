from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    """Product category"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name']


class Product(models.Model):
    """Product model"""
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    stock_quantity = models.PositiveIntegerField(default=0)
    sku = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def average_rating(self):
        """Calculate average rating for product"""
        from ratings.models import ProductRating
        ratings = ProductRating.objects.filter(product=self)
        if ratings.exists():
            return ratings.aggregate(models.Avg('rating'))['rating__avg']
        return 0

    @property
    def rating_count(self):
        """Get total number of ratings"""
        from ratings.models import ProductRating
        return ProductRating.objects.filter(product=self).count()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ['-created_at']


class ProductImage(models.Model):
    """Product images"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    is_primary = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - Image {self.order}"

    class Meta:
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"
        ordering = ['order']


class ProductVideo(models.Model):
    """Product demonstration videos"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    video_file = models.FileField(upload_to='products/videos/')
    thumbnail = models.ImageField(upload_to='products/video_thumbnails/', null=True, blank=True)
    duration = models.PositiveIntegerField(help_text="Duration in seconds", null=True, blank=True)
    file_size = models.PositiveIntegerField(help_text="File size in bytes", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.title}"

    class Meta:
        verbose_name = "Product Video"
        verbose_name_plural = "Product Videos"
        ordering = ['-created_at']
