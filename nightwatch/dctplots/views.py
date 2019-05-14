from django.template import loader
from django.shortcuts import render
from django.http import HttpResponse

from bokeh.embed import server_document


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

    # Setting resources=None means that we must specify/serve them ourselves
    #   as seen in the template <head> section. Easier that way so I can
    #   still use the websocket to the bokeh server container, but keep
    #   all the dependencies in-house.

    dctweather = server_document("http://%s:%d/dctweather" % (hname, hport),
                                 resources=None)
    dctwind = server_document("http://%s:%d/dctwind" % (hname, hport),
                              resources=None)
    dctinstruments = server_document("http://%s:%d/lmitemps" % (hname, hport),
                                     resources=None)
    facsum_tcs = server_document("http://%s:%d/facsum_tcs" % (hname, hport),
                                 resources=None)
    facsum_lpi = server_document("http://%s:%d/facsum_lpi" % (hname, hport),
                                 resources=None)

    print(dctweather)

    return render(request, 'dctplots/index.html',
                  {'dctweatherplot': dctweather,
                   'dctwind': dctwind,
                   'dctinstrumentsplot': dctinstruments,
                   'facsum_tcs': facsum_tcs,
                   'facsum_lpi': facsum_lpi})
