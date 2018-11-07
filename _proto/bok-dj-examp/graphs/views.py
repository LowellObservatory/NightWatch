from django.shortcuts import render, render_to_response
from django.http import HttpResponse

from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from random import randint
import numpy as np

from bokeh.io import output_file, show
from bokeh.models import HoverTool
from .plotWeather import plotWeather

import pandas as pd

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

    return render(request, 'test.html',
           {'script': script, 'div': div, 'script2': script2, 'div2': div2})


def elements(request):
    from bokeh.sampledata.periodic_table import elements
    elements = elements.copy()
    elements = elements[elements["atomic number"] <= 82]
    elements = elements[~pd.isnull(elements["melting point"])]
    mass = [float(x.strip("[]")) for x in elements["atomic mass"]]
    elements["atomic mass"] = mass

    palette = ["#053061", "#2166ac", "#4393c3", "#92c5de", "#d1e5f0",
               "#f7f7f7", "#fddbc7", "#f4a582", "#d6604d", "#b2182b", "#67001f"]

    melting_points = elements["melting point"]
    low = min(melting_points)
    high = max(melting_points)

    #gives items in colors a value from 0-10
    melting_point_inds = [int(10*(x-low)/(high-low)) for x in melting_points]
    elements['melting_colors'] = [palette[i] for i in melting_point_inds]

    TITLE = "Density vs Atomic Weight of Elements (colored by melting point)"
    TOOLS = "hover,pan,wheel_zoom,box_zoom,reset,save"

    p = figure(tools=TOOLS, toolbar_location="above", logo="grey",
        plot_width=1200, plot_height=400, title=TITLE)
    p.background_fill_color = "#dddddd"
    p.xaxis.axis_label = "atomic weight (amu)"
    p.yaxis.axis_label = "density (g/cm^3)"
    p.grid.grid_line_color = "white"
    p.hover.tooltips = [
        ("name", "@name"),
        ("symbol:", "@symbol"),
        ("density", "@density"),
        ("atomic weight", "@{atomic mass}"),
        ("melting point", "@{melting point}")
    ]

    source = ColumnDataSource(elements)

    p.circle("atomic mass", "density", size=12, source=source,
             color='melting_colors', line_color="black", fill_alpha=0.8)

    labels = LabelSet(x="atomic mass", y="density", text="symbol", y_offset=8,
                      text_font_size="8pt", text_color="#555555",
                      source=source, text_align='center')
    p.add_layout(labels)


    # Store components
    script, div = components(p)

    # Feed them to the Django template.
    return render(request, 'bokeh_graph.html',
                              {'script': script, 'div': div})

def hexbin(request):

    n = 400
    x = 2 + 2*np.random.standard_normal(n)
    y = 2 + 2*np.random.standard_normal(n)

    p = figure(title="Hexbin for 500 points", match_aspect=True,
           plot_width=500, plot_height=500,
           tools="wheel_zoom,reset", background_fill_color='#440154')
    p.grid.visible = False

    r, bins = p.hexbin(x, y, size=0.5, hover_color="pink", hover_alpha=0.8)

    p.circle(x, y, color="white", size=1)

    p.add_tools(HoverTool(
        tooltips=[("count", "@c"), ("(q,r)", "(@q, @r)")],
        mode="mouse", point_policy="follow_mouse", renderers=[r]))

    script, div = components(p)

    from bokeh.sampledata.periodic_table import elements
    elements = elements.copy()
    elements = elements[elements["atomic number"] <= 82]
    elements = elements[~pd.isnull(elements["melting point"])]
    mass = [float(x.strip("[]")) for x in elements["atomic mass"]]
    elements["atomic mass"] = mass

    palette = ["#053061", "#2166ac", "#4393c3", "#92c5de", "#d1e5f0",
               "#f7f7f7", "#fddbc7", "#f4a582", "#d6604d", "#b2182b", "#67001f"]

    melting_points = elements["melting point"]
    low = min(melting_points)
    high = max(melting_points)

    #gives items in colors a value from 0-10
    melting_point_inds = [int(10*(x-low)/(high-low)) for x in melting_points]
    elements['melting_colors'] = [palette[i] for i in melting_point_inds]

    TITLE = "Density vs Atomic Weight of Elements (colored by melting point)"
    TOOLS = "hover,pan,wheel_zoom,box_zoom,reset,save"

    p2 = figure(tools=TOOLS, toolbar_location="above", logo="grey",
           plot_width=500, plot_height=500,
         title=TITLE)
    p2.background_fill_color = "#dddddd"
    p2.xaxis.axis_label = "atomic weight (amu)"
    p2.yaxis.axis_label = "density (g/cm^3)"
    p2.grid.grid_line_color = "white"
    p2.hover.tooltips = [
        ("name", "@name"),
        ("symbol:", "@symbol"),
        ("density", "@density"),
        ("atomic weight", "@{atomic mass}"),
        ("melting point", "@{melting point}")
    ]

    source = ColumnDataSource(elements)

    p2.circle("atomic mass", "density", size=12, source=source,
             color='melting_colors', line_color="black", fill_alpha=0.8)

    labels = LabelSet(x="atomic mass", y="density", text="symbol", y_offset=8,
                      text_font_size="8pt", text_color="#555555",
                      source=source, text_align='center')
    p2.add_layout(labels)


    # Store components
    script2, div2 = components(p2)

    # Feed them to the Django template.
    return render(request, 'dyer_graph.html',
                  {'script': script, 'div': div, 'script2': script2, 'div2': div2})

