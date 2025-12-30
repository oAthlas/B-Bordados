from django.urls import path
from . import views
from .views import login_view

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('my-products/', views.my_products, name='my_products'),
    path('perguntas/', views.perguntas, name='perguntas'),
]