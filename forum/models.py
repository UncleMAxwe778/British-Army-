from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import TextField
from django.conf import settings


class Order(models.Model):
    name_order = models.CharField()
    description_of_order = models.TextField()
    rate_for_order = models.IntegerField(default=1, validators=[MinValueValidator(0), MaxValueValidator(10)])
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='order',
        null=True,
        blank=True
    )
    data_giving = models.DateTimeField()

    def __str__(self):
        return F"{self.name_order} {self.user} {self.data_giving}"

class News(models.Model):
    news_name = models.CharField()
    description_of_news = models.TextField()
    rate_for_news = models.IntegerField(default=1, validators=[MinValueValidator(0), MaxValueValidator(10)])
    published_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='news',
        null=True,
        blank=True
    )
    data_giving = models.DateTimeField()

