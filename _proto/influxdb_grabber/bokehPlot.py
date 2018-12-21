# -*- coding: utf-8 -*-
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
#  Created on 4 Dec 2018
#
#  @author: rhamilton

"""One line description of module.

Further description.
"""

from __future__ import division, print_function, absolute_import

import numpy as np
from bokeh.io import curdoc
from bokeh.themes import Theme
from bokeh.models import Plot, Range1d, LinearAxis, DatetimeAxis, \
                         HoverTool, CrosshairTool, CustomJSHover, Quad
from bokeh.models.formatters import DatetimeTickFormatter
from bokeh.plotting import figure, output_file, save, ColumnDataSource


def commonPlot(r, figlabels):
    """
    """
    tools = "pan, wheel_zoom, box_zoom, crosshair, reset, save"

    if figlabels is not None:
        title = figlabels[0]
        xlabel = figlabels[1]
        y1label = figlabels[2]
        y2label = figlabels[3]
    else:
        title, xlabel, y1label, y2label = '', '', '', ''

    p = figure(title=title, x_axis_type='datetime',
               x_axis_label=xlabel, y_axis_label=y1label,
               tools=tools, output_backend="webgl")

    # Make the x-range the maximum data time span to start
    p.x_range = Range1d(start=r.index[0], end=r.index[-1])

    return p, title, xlabel, y1label, y2label


def makePatches(r, y1lim):
    """
    THIS IS a HACK!

    It gives way better tooltips on a timeseries plot.  It works by
    turning the indicies into a list of lists of x coordinates and
    y coordinates for a series of adjacent patches.  Their width is the time
    between two datapoints and height spans the (initial) y1 range.
    """
    ix = []
    iy = []
    for i, _ in enumerate(r.index):
        if i > 0:
            ix.append([r.index[i-1], r.index[i], r.index[i], r.index[i-1]])
            iy.append([y1lim[0], y1lim[0], y1lim[1], y1lim[1]])

    # ColumnDataSource needs everything to have the same length. The last point
    #   might get two tooltips, but I don't care for now.
    ix.append(ix[-1])
    iy.append(iy[-1])

    return ix, iy


def plotLineWithPoints(p, cds, sname, slabel, color,
                       hcolor=None, yrname=None):
    """
    Assumes that you have both 'index' and sname as columns in your
    ColumnDataSource! slabel is then used for the Legend and tooltip labels.
    """
    # NOTE: The way my polling code is set up, mode='after' is the correct
    #   step mode since I get the result and then sleep for an interval
    if hcolor is None:
        hcolor = '#E24D42'

    if yrname is None:
        l = p.step('index', sname, line_width=2, source=cds, mode='after',
                   color=color, legend=slabel, name=slabel)
        s = p.scatter('index', sname, size=8, source=cds,
                      color=color, legend=slabel, name=slabel,
                      alpha=0., hover_alpha=1., hover_color=hcolor)
    else:
        l = p.step('index', sname, line_width=2, source=cds, mode='after',
                   y_range_name=yrname,
                   color=color, legend=slabel, name=slabel)
        s = p.scatter('index', sname, size=8, source=cds,
                      y_range_name=yrname,
                      color=color, legend=slabel, name=slabel,
                      alpha=0., hover_alpha=1., hover_color=hcolor)

    return l, s


def makeInstTempPlot(r, outfile, themefile, cwheel,
                     figlabels=None, y1lim=None, y2lim=None):
    """
    """
    output_file(outfile)
    theme = Theme(filename=themefile)

    p, title, xlabel, y1label, y2label = commonPlot(r, figlabels)

    if y1lim is None:
        y1lim = [r.T1.values.min, r.T1.values.max]
    p.y_range = Range1d(start=y1lim[0], end=y1lim[1])

    if y2lim is None:
        y2lim = [r.T2.values.min, r.T2.values.max]
    p.extra_y_ranges = {"externalTemps": Range1d(start=y2lim[0],
                                                 end=y2lim[1])}
    p.add_layout(LinearAxis(y_range_name="externalTemps",
                            axis_label=y2label), 'right')

    # Hack! But it works. Need to do this *before* you create cds below!
    ix, iy = makePatches(r, y1lim)

    # The "master" data source to be used for plotting
    mds = dict(index=r.index, T1=r.T1, T2=r.T2, ix=ix, iy=iy)
    cds = ColumnDataSource(mds)

    # Make the plots/lines!
    l1, s1 = plotLineWithPoints(p, cds, "T1", y1label, cwheel[0])
    l2, s2 = plotLineWithPoints(p, cds, "T2", y2label, cwheel[1],
                                yrname="externalTemps")

    # HACK HACK HACK HACK HACK
    #   Apply the patches to carry the tooltips
    simg = p.patches('ix', 'iy', source=cds,
                     fill_color=None,
                     fill_alpha=0.0,
                     line_color=None)

    # Make the hovertool only follow this line (bit of a hack)
    htline = simg

    # Customize the active tools
    p.toolbar.autohide = True

    ht = HoverTool()
    ht.tooltips = [("Time", "@index{%F %T}"),
                   (y1label, "@T1"),
                   (y2label, "@T2")]
    ht.formatters = {'index': 'datetime'}
    ht.show_arrow = False
    ht.point_policy = 'follow_mouse'
    ht.line_policy = 'nearest'
    ht.renderers = [htline]
    p.add_tools(ht)

    # Actually apply the theme to the panel
    curdoc().theme = theme
    save(p)

    print("Bokeh plot saved as %s" % (outfile))


def makeWeatherPlots(r, outfile, themefile, cwheel,
                     figlabels=None, y1lim=None, y2lim=None):
    """
    """
    output_file(outfile)
    theme = Theme(filename=themefile)

    p, title, xlabel, y1label, y2label = commonPlot(r, figlabels)

    if y1lim is None:
        y1lim = [r.airTemp_C.values.min, r.airTemp_C.values.max]
    p.y_range = Range1d(start=y1lim[0], end=y1lim[1])

    if y2lim is None:
        y2lim = [r.relativeHumidity.values.min, r.relativeHumidity.values.max]
    p.extra_y_ranges = {"humidity": Range1d(start=y2lim[0],
                                            end=y2lim[1])}
    p.add_layout(LinearAxis(y_range_name="humidity",
                            axis_label=y2label), 'right')

    # Hack! But it works. Need to do this *before* you create cds below!
    ix, iy = makePatches(r, y1lim)

    # The "master" data source to be used for plotting
    mds = dict(index=r.index, Temp=r.airTemp_C, Humi=r.relativeHumidity,
               Dewp=r.dewPointCurrentValue, ix=ix, iy=iy)
    cds = ColumnDataSource(mds)

    # Make the plots/lines!
    l1, s1 = plotLineWithPoints(p, cds, "Temp", y1label, cwheel[0])
    l2, s2 = plotLineWithPoints(p, cds, "Dewp", y1label, cwheel[1])
    l3, s3 = plotLineWithPoints(p, cds, "Humi", y2label, cwheel[2],
                                yrname="humidity")

    # HACK HACK HACK HACK HACK
    #   Apply the patches to carry the tooltips
    simg = p.patches('ix', 'iy', source=cds,
                     fill_color=None,
                     fill_alpha=0.0,
                     line_color=None)

    # Make the hovertool only follow this line (bit of a hack)
    htline = simg

    # Customize the active tools
    p.toolbar.autohide = True

    ht = HoverTool()
    ht.tooltips = [("Time", "@index{%F %T}"),
                   ("AirTemp", "@Temp C"),
                   ("Humidity", "@Humi %"),
                   ("DewPoint", "@Dewp C")
                   ]
    ht.formatters = {'index': 'datetime'}
    ht.show_arrow = False
    ht.point_policy = 'follow_mouse'
    ht.line_policy = 'nearest'
    ht.renderers = [htline]
    p.add_tools(ht)

    # Actually apply the theme to the panel
    curdoc().theme = theme
    save(p)

    print("Bokeh plot saved as %s" % (outfile))
