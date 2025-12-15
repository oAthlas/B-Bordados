from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from django.db import IntegrityError
from django.contrib import messages

from products.models import Product
from home.models import CartItem, banners


# Create your views here.

def home(request):
    sort = request.GET.get('sort', None)
    products = Product.objects.all()
    banners_list = banners.objects.all()

    if sort == "price_asc":
        products = products.order_by('price')
    elif sort == "price_desc":
        products = products.order_by('-price')
    elif sort == "newest":
        products = products.order_by('-id')
    elif sort == "oldest":
        products = products.order_by('id')
    elif sort == "name_asc":
        products = products.order_by('name')
    elif sort == "name_desc":
        products = products.order_by('-name')

    return render(request, 'home/main.html', {
        'products': products,
        'banners': banners_list
        })

def product_show(request, id):
    productshow = get_object_or_404(Product, id=id)
    products = Product.objects.all()
    return render(request, 'home/product.html', {'product': productshow, 'products': products,})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.user.cart

    try:
        CartItem.objects.create(cart=cart, product=product)
        messages.info(request, "Produto adicionado ao carrinho.")

    except IntegrityError:
        messages.warning(request, "O produto já está no carrinho.")

    return redirect('home')


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

    return redirect('home')
