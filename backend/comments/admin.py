from django.contrib import admin
from .models import ProductComment


@admin.register(ProductComment)
class ProductCommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'content_preview', 'parent_comment', 'created_at']
    list_filter = ['created_at', 'is_edited']
    search_fields = ['user__username', 'product__name', 'content']
    readonly_fields = ['created_at', 'updated_at']

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'
