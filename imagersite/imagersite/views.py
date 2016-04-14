from __future__ import unicode_literals
# from django.http import HttpResponse
# from django.template import loader
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.views import login
from imager_images.models import Image
#     kwargstring = argstring = ''
#     if args:
#         argstring = 'args: {}'.format(', '.join(args))
#     if kwargs:
#         kwargstring = 'kwargs: \n{}'.format(''.join(['\t{}: {}'.format(key, val) for key, val in kwargs.items()]))
#     body = """
# home page view was called with:
#     {}
#     {}
#     """.format(argstring, kwargstring)


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

def home_page(request):
    try:
        img = Image.objects.all().filter(published='public').order_by("?")[0].photo
    except IndexError:
        img = 'https://www.petfinder.com/wp-content/uploads/2012/11/99233806-bringing-home-new-cat-632x475.jpg'
    return render(request, 'home.html', context={'img': img})





def logout(request):
    logout(request)
    return redirect('home_page')
