import requests
from django.conf import settings

def create_abacate_payment(order):
    products = []

    for item in order.items.all():
        products.append({
            "externalId": str(item.product.id),
            "name": item.product.name,
            "description": item.product.description,
            "quantity": 1,
            "price": int(item.price * 100)
        })

    payload = {
        "frequency": "ONE_TIME",
        "methods": ["PIX"],
        "products": products,
        "returnUrl": settings.ABACATE_RETURN_URL,
        "completionUrl": settings.ABACATE_COMPLETION_URL,
        "externalId": order.external_id,
        "customer": {
            "name": order.user.get_full_name(),
            "email": order.user.email,
            "cellphone": order.user.customer.phone,
            "taxId": order.user.customer.cpf
        },
        "allowCoupons": False
    }

    headers = {
        "Authorization": f"Bearer {settings.ABACATE_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        settings.ABACATE_API_URL,
        json=payload,
        headers=headers,
        timeout=10
    )

    data = response.json()

    print("STATUS:", response.status_code)
    print("RESPONSE:", data)


    return data["data"]["url"], data["data"]["id"]
