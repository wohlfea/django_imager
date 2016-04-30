from imager_images.models import Image
from api.serializers import PhotoSerializer
from django.contrib.auth.models import User
from rest_framework import permissions
from api.permissions import IsOwner
from rest_framework import mixins, generics, permissions, viewsets


# Create your views here.
class PhotoList(viewsets.ModelViewSet):
    """API endpoint allowing for user photos to be viewed."""
    queryset = Image.objects.filter(published='Public')
    serializer_class = PhotoSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)

    def get_queryset(self):
        queryset = super(PhotoList, self).get_queryset()
        return queryset.filter(owner=self.request.user)


class PhotoDetail(generics.GenericAPIView):
    pass
