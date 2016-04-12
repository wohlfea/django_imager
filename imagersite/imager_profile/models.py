from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings

PHOTOGRAPHY_TYPES = [
    ('portrait', 'Portrait'),
    ('landscape', 'Landscape'),
    ('nature', 'Nature'),
    ('family', 'Family'),
    ('travel', 'Travel'),
    ('art', 'Art'),
    ('food', 'Food'),
]


class ActiveUserManager(models.Manager):
    def get_queryset(self):
        qs = super(ActiveUserManager, self).get_queryset()
        return qs.filter(user__is_active__exact=True)


@python_2_unicode_compatible
class ImagerProfile(models.Model):
    """Profile attached to django's user model."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name='profile',
                                null=False)
    location = models.CharField(default='', max_length=255)
    bio = models.TextField(default='')
    camera = models.TextField(default='')
    photography_type = models.CharField(max_length=30, default='nature',
                                        choices=PHOTOGRAPHY_TYPES)
    friends = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                     related_name='friend_of')
    objects = models.Manager()
    active = ActiveUserManager()

    @property
    def is_active(self):
        """Return True if associated user is active."""
        return self.user.is_active
