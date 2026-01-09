from django.urls import path
from . import views

urlpatterns = [
    path('download/<int:product_id>/', views.download_product, name='download_product'),
]