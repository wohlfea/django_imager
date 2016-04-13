from __future__ import unicode_literals
# from django.http import HttpResponse
# from django.template import loader
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.views import login
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
    return render(request, 'home.html', context={})


def logout(request):
    logout(request)
    return redirect('home_page')
