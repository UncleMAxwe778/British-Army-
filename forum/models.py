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
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='order',
        null=True,
        blank=True
    )
    data_giving = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return F"{self.name_order} {self.user} {self.data_giving}"


class RegimentSelection(models.Model):
    REGIMENT_CHOICES = [
        ("RAC", "Royal Armoured Corps"),
        ("BMP", " British Military Police"),
        ("RM", "Royal Marines"),
        ("MPR", "Military Parachute Regiment"),
        ("UKSF", "United Kingdom Special Forces"),
    ]

    published_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='post_selections',
        null=True,
        blank=True
    )
    regiment = models.CharField(max_length=10, choices=REGIMENT_CHOICES,  null=True, blank=True)
    description = models.TextField(max_length=200)
    date_giving = models.DateTimeField(default=timezone.now)
    max_recruits = models.PositiveIntegerField(default=10)
    recruits = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='signed_up_to_selection',
        blank=True
    )

    def __str__(self):
        return F"{self.published_by} {self.regiment} {self.description} {self.date_giving} {self.max_recruits} - {self.recruits}"

    def is_full(self):
        return self.recruits.count() >= self.max_recruits

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


class Operation(models.Model):
    STATUS_CHOICES = [
        ('PLANNED', 'Planned'),
        ('ACTIVE', 'Active'),
        ('COMPLETED', 'Completed'),
        ('ABORTED', 'Aborted')
    ]
    REGION_OF_UK = [
        ('SCOTLAND', 'Scotland'),
        ('ENGLAND', 'England'),
        ('WALES', 'Wales'),
        ('NI','North Ireland')
    ]


    name = models.CharField(max_length=100)
    description = models.TextField()
    region = models.CharField(
        max_length=20,
        choices=REGION_OF_UK,
        default='ENGLAND'
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='PLANNED'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='operations',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return F"{self.name} {self.description} {self.region} {self.status} {self.created_by}"

class CircleData(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    x = models.FloatField(null=True, blank=True)
    y = models.FloatField(null=True, blank=True)
    operation = models.ForeignKey(
        Operation,
        on_delete=models.CASCADE,
        related_name="circles",
        null=True,
        blank=True
    )
    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return F"{self.operation} {self.x} {self.y} {self.timestamp}"





