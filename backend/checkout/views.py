import requests
import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .models import Order, OrderItem
from .services import MercadoPagoGateway
import uuid
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Order
from django.contrib import messages
from django.conf import settings

@login_required
def checkout_view(request):
    return render(request, "checkout/checkout.html")

@login_required
@login_required
def checkout_pay(request):
    cart = request.user.cart
    cart_items = cart.items.select_related("product")
    customer = request.user.customer

    if not customer.confirmed_data:
        messages.error(request, "Por favor, confirme seus dados antes de prosseguir para o pagamento.")
        return redirect("profile")

    if not cart_items.exists():
        return redirect("home")

    # 🔹 cria pedido
    order = Order.objects.create(
        user=request.user,
        total=sum(item.product.price for item in cart_items),
        external_id=str(uuid.uuid4()),
        status="pending"
    )

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            price=item.product.price
        )

    # 🔹 evita criar pagamento duplicado
    if order.payment_url:
        return redirect(order.payment_url)

    # 🔹 chama o gateway
    gateway = MercadoPagoGateway()
    payment = gateway.create_payment(order)

    # 🔹 salva dados do pagamento
    order.payment_external_id = payment["external_id"]
    order.payment_url = payment["url"]
    order.save(update_fields=[
        "payment_external_id",
        "payment_url"
    ])

    cart_items.delete()

    return redirect(order.payment_url)

@csrf_exempt
def mercadopago_webhook(request):
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponse(status=400)

    payment_id = payload.get("data", {}).get("id")

    if not payment_id:
        return HttpResponse(status=200)

    # 🔎 Buscar pagamento na API do MP (SEGURANÇA)
    response = requests.get(
        f"https://api.mercadopago.com/v1/payments/{payment_id}",
        headers={
            "Authorization": f"Bearer {settings.MP_ACCESS_TOKEN}"
        },
        timeout=10
    )

    payment_data = response.json()

    status = payment_data.get("status")
    external_reference = payment_data.get("external_reference")

    if not external_reference:
        return HttpResponse(status=200)

    try:
        order = Order.objects.get(external_id=external_reference)
    except Order.DoesNotExist:
        return HttpResponse(status=200)

    if status == "approved":
        order.status = "paid"
        order.save(update_fields=["status"])

    elif status in ("cancelled", "rejected"):
        order.status = "canceled"
        order.save(update_fields=["status"])

    return HttpResponse(status=200)

