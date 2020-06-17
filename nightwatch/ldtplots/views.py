from django.template import loader
from django.shortcuts import render
from django.http import HttpResponse

from bokeh.embed import server_document


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

    # Open question - is just pulling via server_document good here,
    #   or should I be doing something else?

    # hname = "localhost"
    hname = "dctsleeperservice"
    hport = 5000

    # For the future
    # hsat = HAniS('hansatdiv', 'hansat')
    # hrad = HAniS('hanraddiv', 'hanrad')

    # Setting resources=None means that we must specify/serve them ourselves
    #   as seen in the template <head> section. Easier that way so I can
    #   still use the websocket to the bokeh server container, but keep
    #   all the dependencies in-house.
    #
    # Reminder: server_document is a *bokeh* function!
    #
    ldtweather = server_document("http://%s:%d/ldtweather" %
                                 (hname, hport), resources=None)
    ldtweathertable = server_document("http://%s:%d/ldtweathertable" %
                                      (hname, hport), resources=None)
    ldtwind = server_document("http://%s:%d/ldtwind" %
                              (hname, hport), resources=None)
    ldtwindtable = server_document("http://%s:%d/ldtwindtable" %
                                   (hname, hport), resources=None)
    facsum_tcs = server_document("http://%s:%d/facsum_tcs" %
                                 (hname, hport), resources=None)
    facsum_lpi = server_document("http://%s:%d/facsum_lpi" %
                                 (hname, hport), resources=None)

    return render(request, 'ldtplots/index.html',
                  {'ldtweatherplot': ldtweather,
                   'ldtweathertable': ldtweathertable,
                   'ldtwind': ldtwind,
                   'ldtwindtable': ldtwindtable,
                   'facsum_tcs': facsum_tcs,
                   'facsum_lpi': facsum_lpi,
                   })
