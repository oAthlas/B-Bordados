from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .models import Order, OrderItem
from .services import create_abacate_payment
from home.models import CartItem, Cart
import uuid
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Order

@login_required
def checkout_view(request):
    return render(request, "checkout/checkout.html")

@login_required
def checkout_pay(request):
    cart = request.user.cart
    cart_items = cart.items.select_related("product")

    if not cart_items.exists():
        return redirect("home")

    external_id = str(uuid.uuid4())

    order = Order.objects.create(
        user=request.user,
        total=sum(item.product.price for item in cart_items),
        external_id=external_id
    )

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            price=item.product.price
        )

    payment_url, abacate_id = create_abacate_payment(order)

    order.abacate_id = abacate_id
    order.save()

    cart_items.delete()

    return redirect(payment_url)


@csrf_exempt
def abacate_webhook(request):
    data = json.loads(request.body)

    external_id = data.get("externalId")
    status = data.get("status")

    try:
        order = Order.objects.get(external_id=external_id)
    except Order.DoesNotExist:
        return HttpResponse(status=404)

    if status == "paid":
        order.status = "paid"
        order.save()

        # aqui você libera o download
        # envia email, etc

    return HttpResponse(status=200)

@csrf_exempt
@require_POST
def abacate_webhook(request):
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")

    # 🔎 estrutura padrão da Abacate Pay
    data = payload.get("data")
    if not data:
        return HttpResponseBadRequest("Missing data")

    billing_id = data.get("id")
    status = data.get("status")

    if not billing_id or not status:
        return HttpResponseBadRequest("Missing billing id or status")

    try:
        order = Order.objects.get(abacate_id=billing_id)
    except Order.DoesNotExist:
        return HttpResponse("Order not found", status=200)

    if status == "PAID":
        order.status = "PAID"
        order.save(update_fields=["status"])

    elif status in ("CANCELED", "EXPIRED"):
        order.status = "CANCELED"
        order.save(update_fields=["status"])

    return HttpResponse("OK", status=200)

