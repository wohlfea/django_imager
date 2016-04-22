from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings
from sorl.thumbnail import ImageField
from django.forms import ModelForm
from django.forms import ModelMultipleChoiceField
from django.contrib.admin.widgets import FilteredSelectMultiple


VISIBILITY_CHOICES = (
    ('Private', 'Private'),
    ('Shared', 'Shared'),
    ('Public', 'Public'),
)


@python_2_unicode_compatible
class Album(models.Model):
    """Album to house images."""
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE,
                              related_name='albums',
                              default='')
    title = models.CharField(default='', max_length=255)
    description = models.TextField(default='')
    date_uploaded = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_published = models.DateTimeField(auto_now_add=True)
    published = models.CharField(max_length=7, choices=VISIBILITY_CHOICES,
                                 default='Private')
    cover = models.ImageField(default='default_cat.jpg')

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class Image(models.Model):
    """Image to be stored."""
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE,
                              related_name='images',
                              default='')
    photo = ImageField(upload_to='photo_files/%Y-%m-%d', default='')
    title = models.CharField(default='', max_length=255)
    description = models.TextField(default='')
    date_uploaded = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_published = models.DateTimeField(auto_now_add=True)
    published = models.CharField(max_length=7, choices=VISIBILITY_CHOICES,
                                 default='Private')
    albums = models.ManyToManyField(Album, related_name='images')

    def __str__(self):
        return self.title


class ImageForm(ModelForm):
    class Meta:
        model = Image
        fields = ['title', 'description', 'published', 'photo']
