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
    path('settings/', views.settings, name='settings'),
    path('change-username/', views.change_username, name='change_username'),
    path('change-password/', views.change_password, name='change_password'),
    path('delete-account/', views.delete_account, name='delete_account'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('change-avatar/', views.change_avatar, name='change_avatar')
]