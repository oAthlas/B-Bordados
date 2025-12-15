from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_user_related_models(sender, instance, created, **kwargs):
    if created:
        from home.models import Cart
        from .models import Customer

        Customer.objects.create(user=instance)
        Cart.objects.create(user=instance)