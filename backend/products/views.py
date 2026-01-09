from django.shortcuts import render
import os
from django.http import FileResponse, Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from checkout.models import OrderItem
from products.models import Product

@login_required
def download_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Verifica se o usuário tem algum pedido PAGO desse produto
    has_paid = OrderItem.objects.filter(
        order__user=request.user,
        order__status='paid',
        product=product
    ).exists()

    if not has_paid:
        raise Http404("Você não tem acesso a este arquivo.")

    if not product.file:
        raise Http404("Arquivo não encontrado.")

    return FileResponse(
        product.file.open('rb'),
        as_attachment=True,
        filename=os.path.basename(product.file.name)
    )