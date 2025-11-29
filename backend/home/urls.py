from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('product_show/<int:id>/', views.product_show, name='product_show'),

]