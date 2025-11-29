from django.shortcuts import render, get_object_or_404
from products.models import Product

# Create your views here.

def home(request):
    sort = request.GET.get('sort', None)
    products = Product.objects.all()

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

    return render(request, 'home/main.html', {'products': products})

def product_show(request, id):
    productshow = get_object_or_404(Product, id=id)
    return render(request, 'home/product_show.html', {'product': productshow})