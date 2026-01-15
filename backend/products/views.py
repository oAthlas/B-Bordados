from django.shortcuts import get_object_or_404, redirect
from django.http import Http404
from .models import Product
from checkout.models import OrderItem
from services.download import get_signed_url
from django.contrib.auth.decorators import login_required

@login_required
def download_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Verifica se o usuário comprou e pagou esse produto
    has_paid = OrderItem.objects.filter(
        order__user=request.user,
        order__status='paid',
        product=product
    ).exists()

    if not has_paid:
        raise Http404("Você não tem acesso a este arquivo.")

    if not product.file_path:
        raise Http404("Arquivo não encontrado.")

    url = get_signed_url(product.file_path)
    return redirect(url)
