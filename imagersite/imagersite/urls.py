"""imagersite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin, auth
from .views import home_page
from django.conf import settings
from django.conf.urls.static import static
# from .views import ClassView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', home_page, name='home_page'),
    url(r'^accounts/login/', auth.views.login),
    url(r'^accounts/logout/', auth.views.logout, {'next_page': home_page}, name='logout'),
    url(r'^accounts/', include('registration.backends.hmac.urls')),
    url(r'^accounts/profile', home_page)
    # url(r'^home/(?P<id>[0-9]+)', ClassView.as_view(), name='home_page'),
    # url(r'^home/([0-9]+)', home_page, name='home_page')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
