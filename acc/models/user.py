from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    user_id = models.CharField(primary_key=True, max_length=60)
    password = models.CharField(max_length=128)

    last_login = models.DateTimeField(blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)

    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    ip = models.CharField(max_length=255, blank=True, null=True)

    is_online = models.BooleanField(blank=True, null=True)
    is_superuser = models.IntegerField(blank=True, null=True)
    is_staff = models.IntegerField(blank=True, null=True)
    is_active = models.IntegerField(blank=True, null=True)
