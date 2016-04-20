from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import ImageForm, AlbumForm


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


def add_photo(request):
    form = ImageForm(request.POST, request.FILES)
    if request.method == 'POST' and form.is_valid():
        form.instance.owner = request.user
        form.save()
        return redirect('library')
    return render(request, 'images/add_image.html', context={'form': form})


def add_album(request):
    form = AlbumForm(request.POST)
    form.instance.owner = request.user
    images = request.user.images.all()
    if request.method == 'POST' and form.is_valid():
        # form.cleaned_data.get('images')
        form.save()
        return redirect('library')
    return render(request, 'images/add_album.html', context={'form': form, 'images': images})
