from django.contrib import admin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'cpf', 'phone')
    search_fields = ('user__email', 'cpf')