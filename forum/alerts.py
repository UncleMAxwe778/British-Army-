from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order


@receiver(post_save, sender=Order)
def course_created_signal(sender, instance, created, **kwargs):
    if created:
        print(f"New order has been created: {instance.name_order} rating of order:{instance.rate_for_order}")
