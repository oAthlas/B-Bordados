from django.urls import path
from .views import checkout_view
from .views import checkout_pay
from .views import mercadopago_webhook

urlpatterns = [
    path('checkout/', checkout_view, name='checkout'),
    path('checkout/pay/', checkout_pay, name='checkout_pay'),
    path("webhooks/mercadopago/", mercadopago_webhook, name="mp_webhook"),]