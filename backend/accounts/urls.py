from django.urls import path
from . import views
from .views import login_view

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', login_view, name='login'),
    path('profile/', views.profile, name='profile'),
]