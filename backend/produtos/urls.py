from django.urls import path
from .views import listar_produtos, listar_categorias

urlpatterns = [
    path('listar/', listar_produtos),
    path('categorias/', listar_categorias),
]