from __future__ import unicode_literals
from django.shortcuts import render, redirect
from imager_images.models import Image
from django.contrib.auth.decorators import login_required


@login_required
def library(request):
    return render(request, 'images/library.html',
                  context={'albums': request.user.albums.all(),
                           'images': request.user.images.all()})


@login_required
def profile_view(request):
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
