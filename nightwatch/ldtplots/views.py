from django.template import loader
from django.shortcuts import render
from django.http import HttpResponse

#from bokeh.embed import server_document


def HAniS(divname, jsconfigvar):
    """
    Return a barebones template for embedding a working HAniS animating thing.
    """
    setupString = "HAniS.setup(%s, '%s')" % (jsconfigvar, divname)

    return {'setupStr': setupString, 'divName': divname}


def index(request):
    """
    This will be the page that generated and then served (to nginx)
    when someone navigates to

    http://nightwatch.lowell.edu

    It's defined in the urlpatterns list in urls.py
    """

    return render(request, 'ldtplots/index.html', {})
