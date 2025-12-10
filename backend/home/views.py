from django.shortcuts import render, get_object_or_404, redirect
from products.models import Product
from home.models import banners
from django.contrib.auth.decorators import login_required

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
    return render(request, 'home/product_show.html', {'product': productshow})

def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)
    cart = request.session.get('cart', {})

    cart[str(product.id)] = {
            'name': product.name,
            'image': product.image.url,
            'price': float(product.price),
            'quantity': 1
            }

    request.session['cart'] = cart
    request.session.modified = True
    return redirect('home')
