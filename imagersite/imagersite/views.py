from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.views import login
from django.contrib.auth.models import User
from imager_images.models import Image


def image_view(request, **kwargs):
    image_id = kwargs.get('image_id')
    user = User.objects.filter(id=kwargs.get('user_id')).first()
    image = user.images.filter(id=image_id).first()
    if not image.published == 'Public' and not request.user.id == user.id:
        return HttpResponse('Unauthorized', status=401)
    return render(request, 'images/image_view.html', context={'image': image})


def album_view(request, **kwargs):
    album_id = kwargs.get('album_id')
    user = User.objects.filter(id=kwargs.get('user_id')).first()
    album = user.albums.filter(id=album_id)[0]
    images = user.albums.filter(id=album_id)[0].images.all()
    if not request.user.id == user.id:
        images = images.filter(published='Public')
    return render(request, 'images/album_view.html',
                  context={'album': album, 'images': images})


def library(request):
    if request.user.is_authenticated():
        return render(request, 'images/library.html',
                      context={'albums': request.user.albums.all(),
                               'images': request.user.images.all()})
    else:
        return redirect('login')


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
