from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    identifier = models.CharField(primary_key=True, max_length=60)
    created = models.DateTimeField(default=timezone.now)
    username = models.CharField(unique=False, max_length=150, null=False)
    ip = models.CharField(max_length=255, blank=True, null=True)
    is_superuser = models.BooleanField(blank=True, null=True, default=False)
    is_active = models.BooleanField(null=False, default=True)

    """
    Those fields are auto generated from django but we won't use them in our app.
    """

    password = models.CharField(max_length=128, blank=True, null=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    email = models.CharField(max_length=254, blank=True, null=True)
    is_staff = models.IntegerField(blank=True, null=True)
    date_joined = models.DateTimeField(blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD = 'identifier'
