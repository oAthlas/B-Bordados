from django.urls import path
from . import views
from .views import login_view

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', login_view, name='login'),
    path('teste/', views.teste, name='teste'),
    path('logout/', views.logout_view, name='logout'),
]