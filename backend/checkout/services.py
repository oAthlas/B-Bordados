import requests
from django.conf import settings


class MercadoPagoGateway:
    name = "mercadopago"

    def create_payment(self, order):
        """
        Cria um pagamento no Mercado Pago e retorna:
        {
            "url": "...",
            "external_id": "..."
        }
        """

        items = []

        for item in order.items.all():
            items.append({
                "title": item.product.name,
                "quantity": 1,
                "currency_id": "BRL",
                "unit_price": float(item.price),
            })

        payload = {
            "items": items,
            "external_reference": str(order.external_id),
            "back_urls": {
                "success": settings.MP_SUCCESS_URL,
                "failure": settings.MP_FAILURE_URL,
                "pending": settings.MP_PENDING_URL,
            },
            "auto_return": "approved",
        }

        headers = {
            "Authorization": f"Bearer {settings.MP_ACCESS_TOKEN}",
            "Content-Type": "application/json",
        }

        response = requests.post(
            "https://api.mercadopago.com/checkout/preferences",
            json=payload,
            headers=headers,
            timeout=10,
        )

        data = response.json()

        if response.status_code not in (200, 201):
            raise Exception(f"Erro Mercado Pago: {data}")

        return {
            "url": data["init_point"],
            "external_id": data["id"],
        }