from django.urls import path
from .views import checkout_view
from .views import checkout_pay
from .views import abacate_webhook

urlpatterns = [
    path('checkout/', checkout_view, name='checkout'),
    path('checkout/pay/', checkout_pay, name='checkout_pay'),
    path("webhook/abacate/", abacate_webhook, name="abacate_webhook"),
]