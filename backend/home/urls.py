from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:id>/', views.product_show, name='product'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('pesquisa/', views.pesquisa, name='pesquisa'),
]