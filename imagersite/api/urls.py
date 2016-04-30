from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from api import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'photos', views.PhotoList)

urlpatterns = [
    url(r'^v1/', include(router.urls)),
    # url(r'^v1/(?P<pk>[0-9]+)/$', views.PhotoDetail.as_view())
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

# urlpatterns = format_suffix_patterns(urlpatterns)
