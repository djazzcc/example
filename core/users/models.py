# core/users/models.py

# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError

class User(AbstractUser):
    email_verified = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

class EmailVerification(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE)
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    verified_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Email verification for {self.user.email}"

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = get_random_string(64)
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(days=3)
        super().save(*args, **kwargs)

    @property
    def is_expired(self):
        return timezone.now() > self.expires_at

    @property
    def is_verified(self):
        return self.verified_at is not None
