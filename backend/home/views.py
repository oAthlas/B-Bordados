from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from django.db import IntegrityError
from django.contrib import messages

from products.models import Product, Category
from home.models import CartItem, banners


# Create your views here.

def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    banners_list = banners.objects.all()

    category_slug = request.GET.get("category")
    if category_slug:
        products = products.filter(category__slug=category_slug)

    return render(request, 'home/main.html', {
        'products': products,
        'banners': banners_list,
        'categories': categories,
        })

def product_show(request, id):
    productshow = get_object_or_404(Product, id=id)
    products = Product.objects.all()
    return render(request, 'home/product.html', {'product': productshow, 'products': products,})

def pesquisa(request):
    query = request.GET.get('q')
    categories = Category.objects.all()
    products = Product.objects.all()

    category_slug = request.GET.get("category")
    if category_slug:
        products = products.filter(category__slug=category_slug)

    if query:
        products = products.filter(name__icontains=query)

    return render(request, 'home/pesquisa.html', {
        'products': products, 
        'query': query,
        'categories': categories,
    })

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.user.cart

    try:
        CartItem.objects.create(cart=cart, product=product)
        messages.info(request, "Produto adicionado ao carrinho.")

    except IntegrityError:
        messages.warning(request, "O produto já está no carrinho.")

    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
def remove_from_cart(request, item_id):
    cart  = request.user.cart

    cart_item = get_object_or_404(
        CartItem, 
        cart=request.user.cart, 
        id=item_id
    )

    cart_item.delete()
    messages.info(request, "Produto removido do carrinho.")

    return redirect(request.META.get('HTTP_REFERER', 'home'))


