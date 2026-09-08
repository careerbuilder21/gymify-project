from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Order, OrderItem
from accounts.models import User

def admin_check(request):
    return request.user.is_authenticated and request.user.role == 'admin'

def admin_products(request):
    if not admin_check(request):
        return redirect('login')
    
    products = Product.objects.all()
    orders = Order.objects.all().order_by('-created_at')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add':
            name = request.POST.get('name')
            description = request.POST.get('description')
            price = request.POST.get('price')
            stock = request.POST.get('stock')
            image = request.FILES.get('image')
            Product.objects.create(
                name=name,
                description=description,
                price=price,
                stock=stock,
                image=image
            )
            return redirect('admin_products')
        
        elif action == 'delete':
            product_id = request.POST.get('product_id')
            Product.objects.filter(id=product_id).delete()
            return redirect('admin_products')
    
    return render(request, 'admin/products.html', {
        'products': products,
        'orders': orders
    })

def edit_product(request, product_id):
    if not admin_check(request):
        return redirect('login')
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        product.stock = request.POST.get('stock')
        if request.FILES.get('image'):
            product.image = request.FILES.get('image')
        product.save()
        return redirect('admin_products')
    return render(request, 'admin/edit_product.html', {
        'product': product
    })
