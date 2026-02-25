import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import TextField
from django.conf import settings
from django.utils import timezone

from user_officers.models import CustomUser


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
    data_giving = models.DateTimeField(default=timezone.now)


class MessageList(models.Model):
    sender = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        null=True,
        blank=True
    )
    receiver = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='received_messages',
        null=True,
        blank=True
    )
    name_message = models.CharField(max_length=100)
    whole_message = models.TextField(max_length=255)
    data_giving = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)


class Request(models.Model):

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_requests"
    )
    assigned_officer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="assigned_officer",
        null=True,
        blank=True
    )
    current_status = models.ForeignKey(
        "ReviewerOfRequest",
        on_delete=models.CASCADE,
        related_name="+",
        null=True,
        blank=True
    )
    title = models.CharField(max_length=86)
    description = models.TextField(max_length=230)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


class ReviewerOfRequest(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected")
    ]

    request = models.ForeignKey(
        Request,
        on_delete=models.CASCADE,
        related_name="requests",
        null=True,
        blank=True
    )
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviewer",
        null=True,
        blank=True
    )
    decision = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="PENDING"
    )
    comment = models.TextField(max_length=255)
    reviewed_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.decision