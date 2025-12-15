from django.db import models
from django.conf import settings

class Customer(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    cpf = models.CharField(max_length=11, unique=True, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)