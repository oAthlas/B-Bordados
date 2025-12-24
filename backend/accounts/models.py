from django.db import models
from django.conf import settings

class Customer(models.Model):

    GENDER_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    cpf = models.CharField(max_length=11, unique=True, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    complete_name = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        blank=True,
        null=True,
    )

    confirmed_data = models.BooleanField(default=False)