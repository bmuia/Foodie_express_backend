from django.urls import path
from .views import (
    CategoryListCreateAPIView, 
    CategoryRetrieveUpdateDestroyAPIView, 
    ProductListCreateAPIView, 
    ProductRetrieveUpdateDestroyAPIView,
    ImageListCreateAPIView,
    ImageRetrieveUpdateDestroyAPIView
)

urlpatterns = [
    # Category URLs
    path('categories/', CategoryListCreateAPIView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDestroyAPIView.as_view(), name='category-retrieve-update-destroy'),

    # Product URLs
    path('products/', ProductListCreateAPIView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductRetrieveUpdateDestroyAPIView.as_view(), name='product-retrieve-update-destroy'),

    # Image URLs
    path('images/', ImageListCreateAPIView.as_view(), name='image-list-create'),
    path('images/<int:pk>/', ImageRetrieveUpdateDestroyAPIView.as_view(), name='image-retrieve-update-destroy'),
]
