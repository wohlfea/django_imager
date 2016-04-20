from django.conf.urls import url
from .views import album_view, image_view, add_photo, add_album


urlpatterns = [
    url(r'^album/(?P<user_id>[0-9]+)/(?P<album_id>[0-9]+)', album_view, name='album_view'),
    url(r'^image/(?P<user_id>[0-9]+)/(?P<image_id>[0-9]+)', image_view, name='image_view'),
    url(r'^photo/add/$', add_photo, name='add_photo'),
    url(r'^album/add/$', add_album, name='add_album'),
]
