from django.template import loader
from django.shortcuts import render
from django.http import HttpResponse

from bokeh.embed import components, server_document


def index(request):
    """
    This will be the page that generated and then served (to nginx)
    when someone navigates to

    http://nightwatch.lowell.edu

    It's defined in the urlpatterns list in urls.py
    """

    # Open question - is just pulling via server_document good here,
    #   or should I be doing something else?

    dctweather = server_document("http://dctsleeperservice:5000/dctweather")

    dctwind = server_document("http://dctsleeperservice:5000/dctwind")

    dctinstruments = server_document("http://dctsleeperservice:5000/lmitemps")

    facsum_tcs = server_document("http://dctsleeperservice:5000/facsum_tcs")

    facsum_lpi = server_document("http://dctsleeperservice:5000/facsum_lpi")

    return render(request, 'dctplots/index.html',
                  {'dctweatherplot': dctweather,
                   'dctwind': dctwind,
                   'dctinstrumentsplot': dctinstruments,
                   'facsum_tcs': facsum_tcs,
                   'facsum_lpi': facsum_lpi})
