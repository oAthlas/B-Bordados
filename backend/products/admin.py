# products/admin.py
from django.contrib import admin
from django import forms
from .models import Product, Category
from services.supabase import upload_product_file

class ProductAdminForm(forms.ModelForm):
    upload_file = forms.FileField(
        required=False,
        help_text="Envie o arquivo do produto (somente .ZIP)"
    )

    class Meta:
        model = Product
        fields = "__all__"

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Primeiro salva para obter o ID
        if commit:
            instance.save()
        
        file = self.cleaned_data.get("upload_file")
        if file:
            # Agora temos o ID
            path = upload_product_file(file, instance.id)
            instance.file_path = path
            instance.save()  # Salva novamente com o caminho do arquivo

        return instance

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ['name', 'category', 'price', 'has_file']
    
    def has_file(self, obj):
        return bool(obj.file_path)
    has_file.boolean = True
    has_file.short_description = 'Tem arquivo'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}