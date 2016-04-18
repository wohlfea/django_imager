from __future__ import unicode_literals
from django.http import HttpResponse
# from django.template import loader
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.views import login
from imager_images.models import Image

# def home_page(request, *args, **kwargs):
#     template = loader.get_template('home.html')
#     body = template.render({'foo': 'foo'})
#     return HttpResponse(body)

# This is nicer!
# def home_page(request, *args, **kwargs):
#     return render(request, 'home.html', context={'foo': 'foo'})
#
#
# class ClassView(TemplateView):
#     template_name = 'home.html'
#
#     def get_context_data(self, id=1):
#         foo = 'garbonzo beans'
#         return {'foo': foo}


def image_view(request, **kwargs):
    image_id = kwargs.get('image_id')
    image = request.user.images.filter(id=image_id)[0]
    return render(request, 'images/image_view.html', context={'image': image})


def album_view(request, **kwargs):
    album_id = kwargs.get('album_id')
    album = request.user.albums.filter(id=album_id)[0]
    images = request.user.albums.filter(id=album_id)[0].images.all()
    return render(request, 'images/album_view.html',
                  context={'album': album, 'images': images})


def library(request):
    return render(request, 'images/library.html',
                  context={'albums': request.user.albums.all(),
                           'images': request.user.images.all()})


def profile_view(request):
    if request.user.is_authenticated():
        try:
            img = Image.objects.all().filter(owner=request.user.profile.user
                                             ).order_by("?")[0].photo.url
        except IndexError:
            img = 'https://www.petfinder.com/wp-content/uploads/2012/11/99233806-bringing-home-new-cat-632x475.jpg'
        image_count = len(request.user.images.all())
        album_count = len(request.user.albums.all())
        return render(request, 'profile_view.html',
                      context={'img': img,
                               'image_count': image_count,
                               'album_count': album_count})
    else:
        return redirect('login')


def home_page(request):
    try:
        img = Image.objects.all().filter(published='Public'
                                         ).order_by("?")[0].photo.url
    except IndexError:
        img = 'https://www.petfinder.com/wp-content/uploads/2012/11/99233806-bringing-home-new-cat-632x475.jpg'
    return render(request, 'home.html', context={'img': img})


def logout(request):
    logout(request)
    return redirect('home_page')
