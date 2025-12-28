from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import TextField
from django.conf import settings


class Steamer(models.Model):

    first_name_steamers = models.CharField()
    last_name_steamers = models.CharField()
    call_sign = models.CharField()
    rank = models.CharField()
    biography = models.TextField()
    combat_experience = models.CharField()
    joined_regiment = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name_steamers} {self.last_name_steamers}"


class Private(models.Model):

    first_name_private = models.CharField()
    last_name_private = models.CharField()
    call_sign = models.CharField()
    rank = models.CharField()
    biography = models.TextField()
    university_education = models.CharField()
    steamer = models.ForeignKey(
        Steamer,
        on_delete=models.CASCADE,
        related_name='private',
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.call_sign} {self.first_name_private} {self.last_name_private}"

class Order(models.Model):
    name_order = models.CharField()
    description_of_order = models.TextField()
    rate_for_order = models.IntegerField(default=1, validators=[MinValueValidator(0), MaxValueValidator(10)])
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='private',
        null=True,
        blank=True
    )
    data_giving = models.DateTimeField()

    def __str__(self):
        return F"{self.name_order} {self.user} {self.data_giving}"


