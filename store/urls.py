from django.urls import path
from . import views

urlpatterns = [
    path('admin-panel/products/', views.admin_products, name='admin_products'),
    path('admin-panel/products/edit/<int:product_id>/', views.edit_product, name='edit_product'),
]