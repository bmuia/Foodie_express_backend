from django.db import models
from django.core.exceptions import ValidationError
from PIL import Image as PILImage

class Category(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.description[:20]}..."

    def clean(self):
        if Category.objects.filter(title=self.title).exists():
            raise ValidationError("A category with this title already exists.")

class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_products', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_discounted = models.BooleanField(default=False)
    discount_type = models.CharField(max_length=10, choices=[('percent', 'Percentage'), ('fixed', 'Fixed')], null=True, blank=True)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ['title', 'category']

    def __str__(self):
        return self.title

    def get_discounted_price(self):
        if not self.is_discounted:
            return self.price
        
        if self.discount_type == 'percent' and self.discount_value:
            return self.price - (self.price * (self.discount_value / 100))
        
        if self.discount_type == 'fixed' and self.discount_value:
            return self.price - self.discount_value
        
        return self.price  

    def save(self, *args, **kwargs):
        if self.is_discounted and self.discount_value:
            self.discount_price = self.get_discounted_price()
        super(Product, self).save(*args, **kwargs)

    def clean(self):
        if Product.objects.filter(title=self.title, category=self.category).exists():
            raise ValidationError("A product with this title already exists in this category.")

class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['image', 'product']

    def __str__(self):
        return f"Image for {self.product.title}"

    def clean(self):
        img = PILImage.open(self.image)
        
        if self.image.size > 20 * 1024 * 1024:  # 20MB
            raise ValidationError("Image size cannot exceed 20MB.")
        
  
        if img.format not in ['JPEG', 'PNG']:
            raise ValidationError("Image format must be JPEG or PNG.")
        

        if Image.objects.filter(image=self.image, product=self.product).exists():
            raise ValidationError("This image has already been uploaded for this product.")
