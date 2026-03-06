from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):


    ROLE_CHOICES = [
        ("CTZ", "Citizen"),
        ("PRESS", "Journalist"),
        ("MLT", "Military")
    ]

    RANK_CHOICES = [
        ("RCT", "Recruit"),
        ("PVT", "Private"),
        ("LCPL", "Lance Corporal"),
        ("CPL", "Corporal"),
        ("SGT", "Sergeant"),
        ("SSGT", "Staff Sergeant"),
        ("WOC2", "Warrant Officer Class 2"),
        ("WOC1", "Warrant Officer Class 1"),
        ("2LT", "Second Lieutenant"),
        ("LT", "Lieutenant"),
        ("CPT", "Captain"),
        ("MAJ", "Major"),
        ("LTC", "Lieutenant Colonel"),
        ("COL", "Colonel"),
        ("BRIG", "Brigadier"),
        ("MG", "Major General"),
        ("LG", "Lieutenant General"),
        ("GEN", "General"),
    ]

    REGIMENT_CHOICES = [
        ("BA", "British Army"),
        ("RAC", "Royal Armoured Corps"),
        ("BMP", " British Military Police"),
        ("RM", "Royal Marines"),
        ("MPR", "Military Parachute Regiment"),
        ("UKSF", "United Kingdom Special Forces"),
    ]


    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=75)
    last_name = models.CharField(max_length=95)
    role = models.CharField(max_length=10,choices=ROLE_CHOICES, default="MLT")
    rank = models.CharField(max_length=10, choices=RANK_CHOICES, default="RCT", null=True, blank=True)
    regiment = models.CharField(max_length=10, choices=REGIMENT_CHOICES, default="BA",  null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    def __str__(self):
        return f" {self.first_name} {self.last_name} {self.email} {self.rank} {self.regiment} {self.role}"

    def update_admin_status(self):
        highest_ranks = ["COL", "BRIG", "MG", "LG", "GEN"]
        if self.rank in highest_ranks:
            self.is_staff = True
            self.is_superuser = True
        else:
            self.is_staff = False
            self.is_superuser = False

    def staff_for_create(self):
        return self.rank in settings.ALLOWED_ORDER_RANKS

    def can_create_news(self):
        return self.role in settings.ALLOWED_NEWS_ROLES

    def only_for_military(self):
        return self.role in settings.ALLOWED_ONLY_MILITARY

    def save(self, *args, **kwargs):
        self.update_admin_status()
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()

        # Citizens & Press should NOT have military data
        if self.role in ["CTZ", "PRESS"]:
            self.rank = None
            self.regiment = None

