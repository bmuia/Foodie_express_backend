from django.contrib import admin
from .models import Category, Product, Image

# Category admin class
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at', 'updated_at')

# Product admin class
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'price', 'is_available', 'is_featured', 'is_discounted','discount_value', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    list_filter = ('category', 'is_available', 'is_featured', 'is_discounted', 'created_at', 'updated_at')


# Image admin class
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'image', 'created_at', 'updated_at')
    search_fields = ('product__title',)  
    list_filter = ('created_at', 'updated_at')

# Register the models with the admin site
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Image, ImageAdmin)