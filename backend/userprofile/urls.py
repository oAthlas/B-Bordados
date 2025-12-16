from django.urls import path
from . import views

urlpatterns = [
    path('pessoal', views.pessoal, name='pessoal'),
]