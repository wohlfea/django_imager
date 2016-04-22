from __future__ import unicode_literals
from django import http
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import ImageForm, Album, Image
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView
from django.utils.decorators import method_decorator
from django import forms
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.views.generic.edit import FormView


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


@login_required
def add_photo(request):
    form = ImageForm(request.POST, request.FILES)
    if request.method == 'POST' and form.is_valid():
        form.instance.owner = request.user
        form.save()
        return redirect('library')
    return render(request, 'images/add_image.html', context={'form': form})


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        exclude = ['owner']
    images = forms.ModelMultipleChoiceField(queryset=Image.objects.all())

    def __init__(self, *args, **kwargs):
        if kwargs.get('instance'):
            initial = kwargs.setdefault('initial', {})
            initial['images'] = [image.pk for image in kwargs['instance'].images.all()]
        forms.ModelForm.__init__(self, *args, **kwargs)

    def save(self, commit=True):
        instance = forms.ModelForm.save(self, False)
        old_save_m2m = self.save_m2m

        def save_m2m():
            old_save_m2m()
            instance.images.clear()
            for topping in self.cleaned_data['images']:
                instance.images.add(topping)
        self.save_m2m = save_m2m
        if commit:
            instance.save()
            self.save_m2m()
        return instance


@method_decorator(login_required, name='dispatch')
class AddAlbum(FormView):
    template_name = 'images/add_album.html'
    form_class = AlbumForm
    success_url = '/images/library/'

    def get_form(self, form_class=None):
        form = super(AddAlbum, self).get_form()
        form.fields['images'].queryset = self.request.user.images.all()
        return form

    def form_valid(self, form, *args, **kwargs):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        images = form.cleaned_data['images']
        [image.albums.add(self.object) for image in images]
        return super(AddAlbum, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class EditImage(UpdateView):
    model = Image
    template_name = 'images/edit_image.html'
    fields = ['title', 'description', 'published']
    success_url = '/images/library'

    def get(self, request, *args, **kwargs):
        try:

            image = Image.objects.get(owner=self.request.user.id,
                                      pk=kwargs['pk'])
        except ObjectDoesNotExist:
            raise http.HttpResponseNotFound('<p>Page Not Found</p>')
        if request.user != image.owner:
            raise PermissionDenied
        else:
            return super(EditImage, self).get(request)

    def form_valid(self, form, *args, **kwargs):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return super(EditImage, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class EditAlbum(UpdateView):
    model = Album
    template_name = 'images/edit_album.html'
    fields = ['title', 'description', 'published', 'cover']
    success_url = '/images/library'

    def get(self, request, *args, **kwargs):
        try:
            album = Album.objects.get(pk=kwargs['pk'])
        except ObjectDoesNotExist:
            raise http.HttpResponseNotFound('<h1>Page not found.</h1>')
        if request.user.id != album.owner.id:
            raise PermissionDenied
        else:
            return super(EditAlbum, self).get(request)

    def form_valid(self, form, *args, **kwargs):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return super(EditAlbum, self).form_valid(form)
