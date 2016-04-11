from django.db import models
from imager_profile.models import ImagerProfile


VISIBILITY_CHOICES = (
    ('Private', 'Private'),
    ('Shared', 'Shared'),
    ('Public', 'Public'),
)


class Album(models.Model):
    """Album to house images."""
    owner = models.ForeignKey(imager_profile, on_delete=models.CASCADE)
    title = models.CharField(default='', max_length=255)
    description = models.TextField(default='')
    date_uploaded = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_published = models.DateTimeField(auto_now_add=True)
    published = models.CharField(max_length=7, choices=VISIBILITY_CHOICES,
                                 default='Private')
    contains = models.ManyToManyField(Image)

    def __str__(self):
        return self.title


class Image(models.Model):
    """Image to be stored."""
    owner = models.ForeignKey(imager_profile, on_delete=models.CASCADE)
    title = models.CharField(default='', max_length=255)
    description = models.TextField(default='')
    date_uploaded = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_published = models.DateTimeField(auto_now_add=True)
    published = models.CharField(max_length=7, choices=VISIBILITY_CHOICES,
                                 default='Private')
    in_album = models.ManyToManyField(Album)

    def __str__(self):
        return self.title
