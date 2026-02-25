from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib import messages
from django.template.context_processors import request

from . import apps
from .models import Order, MessageList
from user_officers.models import CustomUser


@receiver(post_save, sender=Order)
def course_created_signal(sender, instance, created, **kwargs):
    if created:
        print(f"New order has been created: {instance.name_order} rating of order:{instance.rate_for_order}, Posted by:{instance.user}")





@receiver(pre_save, sender=CustomUser, )
def receiver(sender, instance, **kwargs):
    if not instance.pk:
        return  # new user creation

    old_user = sender.objects.get(pk=instance.pk)

    changed_fields = []
    watched_fields = ["rank", "regiment", "role"]

    for field in watched_fields:
        if getattr(old_user, field) != getattr(instance, field):
            changed_fields.append(field)

    if not changed_fields:
        return

    fields_text = ", ".join(changed_fields)

    MessageList.objects.create(
        sender=None,
        receiver=instance,
        name_message="Account Update Notification",
        whole_message=f"Your account fields changed: {fields_text} by high command."
    )
