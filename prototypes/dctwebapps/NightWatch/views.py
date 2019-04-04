from django.shortcuts import render, render_to_response
from django.http import HttpResponse

from bokeh.plotting import figure, output_file, show
from bokeh.embed import components, server_document
from random import randint
import numpy as np

from bokeh.io import output_file, show
from bokeh.models import HoverTool
from .plotWeather import plotWeather

import pandas as pd
import re

from bokeh.models import ColumnDataSource, LabelSet
from bokeh.sampledata.periodic_table import elements


def debug(x, name):
    print('\n' * 5)
    print('{} = {}'.format(name, x))
    print('type({}) = {}'.format(name, type(x)))
    print('\n' * 5)

def home(request):
    return render_to_response('dyer_test.html')

def test(request):
    p = plotWeather.readTempData()

    script, div = components(p)

    p2 = plotWeather.readHumidity()

    script2, div2 = components(p2)

    script4 = server_document("http://localhost:5006/ohlc")

    script3 = server_document("http://localhost:5006/newact")

    print(script3)
    print(script4)



    return render(request, 'test.html',
           {'script': script, 'div': div, 'script2': script2, 'div2': div2, 'script3': script3, 'script4': script4})
