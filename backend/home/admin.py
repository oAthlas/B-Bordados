from django.contrib import admin
from .models import banners
from .models import Cart
from .models import CartItem

admin.site.register(banners)
admin.site.register(Cart)
admin.site.register(CartItem)