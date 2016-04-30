from imager_images.models import Image
from rest_framework import serializers


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('title', 'description', 'published', 'photo')
