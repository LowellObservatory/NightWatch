from django.shortcuts import render
from django.http import HttpResponse

import influxdb_grabber as idbg


def index(request):
    """
    This will be the page that is returned when someone navigates to

    http://nightwatch/dctplots/index.html (or just nightwatch/dctplots)

    It's defined in the urlpatterns list in urls.py
    """

    p = plotWeather.readTempData()
    script, div = components(p)

    p2 = plotWeather.readHumidity()
    script2, div2 = components(p2)

    script4 = server_document("http://localhost:5006/ohlc")

    script3 = server_document("http://localhost:5006/newact")

    print(script3)
    print(script4)


    return render(request, 'index.html',
                  {'script': script,
                   'div': div,
                   'script2': script2,
                   'div2': div2,
                   'script3': script3,
                   'script4': script4})
