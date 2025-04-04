from rest_framework import serializers
from .models import Category, Product, Image

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'description', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
        extra_kwargs = {
            'title': {'required': True},
            'description': {'required': True}
        }

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=False)
    images = serializers.PrimaryKeyRelatedField(many=True, queryset=Image.objects.all(), required=False)

    class Meta:
        model = Product
        fields = [
            'id', 'title', 'description', 'price', 'category', 'created_at', 'updated_at', 
            'is_available', 'is_featured', 'is_discounted', 'discount_type', 
            'discount_value', 'quantity', 'images', 'discount_price'
        ]
        read_only_fields = ['created_at', 'updated_at', 'discount_price']
        extra_kwargs = {
            'title': {'required': True},
            'description': {'required': True},
            'price': {'required': True},
        }

    def validate(self, attrs):
        if attrs.get('is_discounted') and not attrs.get('discount_value'):
            raise serializers.ValidationError("Discount value must be provided if the product is discounted.")
        if attrs.get('is_discounted') and not attrs.get('discount_type'):
            raise serializers.ValidationError("Discount type must be provided if the product is discounted.")
        return attrs

    def create(self, validated_data):
        images_data = validated_data.pop('images', None)
        product = super().create(validated_data)
        if images_data:
            product.images.set(images_data)  
        return product

    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', None)
        instance = super().update(instance, validated_data)
        if images_data:
            instance.images.set(images_data)
        return instance

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image', 'product', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
        extra_kwargs = {
            'image': {'required': True},
            'product': {'required': True},
        }

    def validate(self, attrs):
        img = attrs.get('image')
        if img:
            # Validate the image size (20MB max)
            if img.size > 20 * 1024 * 1024:  # 20MB
                raise serializers.ValidationError("Image size cannot exceed 20MB.")
        return attrs
