from django.db import models
from django.contrib.auth.models import User


class ImagerProfile(models.Model):
    """Profile attached to django's user model."""
    user = models.OneToOneField(User, related_name='profile')
    location = models.CharField(default='', max_length=255)
    bio = models.TextField(default='')

    @classmethod
    def active(cls):
        """Return profiles of all active users"""
        return cls.objects.filter(is_active=True)

    @property
    def is_active(self):
        """Return True if associated user is active."""
        return self.user.is_active
