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
import datetime as dt

from bokeh.io import curdoc
from bokeh.themes import Theme
from bokeh.models import Plot, Range1d, LinearAxis, DatetimeAxis, \
    HoverTool, CrosshairTool, CustomJSHover, Quad, Legend, LegendItem
from bokeh.models.formatters import DatetimeTickFormatter
from bokeh.plotting import figure, output_file, save, ColumnDataSource


def commonPlot(r, ldict):
    """
    """
    tools = "pan, wheel_zoom, box_zoom, crosshair, reset, save"

    title = ldict['title']
    xlabel = ldict['xlabel']
    y1label = ldict['y1label']

    p = figure(title=title, x_axis_type='datetime',
               x_axis_label=xlabel, y_axis_label=y1label,
               tools=tools, output_backend="webgl")

    # Make the x-range the maximum data time span to start
    p.x_range = Range1d(start=r.index[0], end=r.index[-1])

    return p


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


def plotLineWithPoints(p, cds, sname, color,
                       hcolor=None, yrname=None):
    """
    p: plot object
    cds: ColumnDataSource
    sname: source name (in cds)
    slabel: series label (for legend)
    Assumes that you have both 'index' and sname as columns in your
    ColumnDataSource! slabel is then used for the Legend and tooltip labels.
    """
    # NOTE: The way my polling code is set up, mode='after' is the correct
    #   step mode since I get the result and then sleep for an interval
    if hcolor is None:
        hcolor = '#E24D42'

    if yrname is None:
        l = p.step('index', sname, line_width=2, source=cds, mode='after',
                   color=color, name=sname)
        s = p.scatter('index', sname, size=8, source=cds,
                      color=color, name=sname,
                      alpha=0., hover_alpha=1., hover_color=hcolor)
    else:
        l = p.step('index', sname, line_width=2, source=cds, mode='after',
                   y_range_name=yrname,
                   color=color, name=sname)
        s = p.scatter('index', sname, size=8, source=cds,
                      y_range_name=yrname,
                      color=color, name=sname,
                      alpha=0., hover_alpha=1., hover_color=hcolor)

    return l, s


# def makeInstTempPlot(r, outfile, themefile, cwheel,
#                      figlabels=None, y1lim=None, y2lim=None):
#     """
#     """
#     output_file(outfile)
#     theme = Theme(filename=themefile)

#     p, title, xlabel, y1label, y2label = commonPlot(r, figlabels)

#     if y1lim is None:
#         y1lim = [r.T1.values.min, r.T1.values.max]
#     p.y_range = Range1d(start=y1lim[0], end=y1lim[1])

#     if y2lim is None:
#         y2lim = [r.T2.values.min, r.T2.values.max]
#     p.extra_y_ranges = {"externalTemps": Range1d(start=y2lim[0],
#                                                  end=y2lim[1])}
#     p.add_layout(LinearAxis(y_range_name="externalTemps",
#                             axis_label=y2label), 'right')

#     # Hack! But it works. Need to do this *before* you create cds below!
#     ix, iy = makePatches(r, y1lim)

#     # The "master" data source to be used for plotting
#     mds = dict(index=r.index, T1=r.T1, T2=r.T2, ix=ix, iy=iy)
#     cds = ColumnDataSource(mds)

#     # Make the plots/lines!
#     l1, s1 = plotLineWithPoints(p, cds, "T1", y1label, cwheel[0])
#     l2, s2 = plotLineWithPoints(p, cds, "T2", y2label, cwheel[1],
#                                 yrname="externalTemps")

#     # HACK HACK HACK HACK HACK
#     #   Apply the patches to carry the tooltips
#     simg = p.patches('ix', 'iy', source=cds,
#                      fill_color=None,
#                      fill_alpha=0.0,
#                      line_color=None)

#     # Make the hovertool only follow this line (bit of a hack)
#     htline = simg

#     # Customize the active tools
#     p.toolbar.autohide = True

#     ht = HoverTool()
#     ht.tooltips = [("Time", "@index{%F %T}"),
#                    (y1label, "@T1"),
#                    (y2label, "@T2")]
#     ht.formatters = {'index': 'datetime'}
#     ht.show_arrow = False
#     ht.point_policy = 'follow_mouse'
#     ht.line_policy = 'nearest'
#     ht.renderers = [htline]
#     p.add_tools(ht)

#     # Actually apply the theme to the panel
#     curdoc().theme = theme
#     save(p)

#     print("Bokeh plot saved as %s" % (outfile))


def makeWeatherPlots(indat, outfile, themefile, cwheel):
    """
    """

    y1lim = [-15, 15]
    y2lim = [0, 100]

    # Get the keys that define the input dataset
    #   TODO: make the first defined tag the "primary" meaning X1/Y1 plot
    #         ...but I can't quite figure out the abstraction well enough.
    r = indat['q_wrs']
    r2 = indat['q_mounttemp']
    output_file(outfile)
    theme = Theme(filename=themefile)

    ldict = {'title': "WRS Weather Information",
             'xlabel': "Time (UTC)",
             'y1label': "Temperature (C)",
             'y2label': "Humidity (%)"}

    p = commonPlot(r, ldict)
    timeNow = dt.datetime.utcnow()
    tWindow = dt.timedelta(hours=24)

    if y1lim is None:
        y1lim = [r.AirTemp.values.min, r.AirTemp.values.max]
    p.y_range = Range1d(start=y1lim[0], end=y1lim[1])
    p.x_range = Range1d(start=timeNow-tWindow, end=timeNow)

    if y2lim is None:
        y2lim = [r.Humidity.values.min, r.Humidity.values.max]
    p.extra_y_ranges = {"y2": Range1d(start=y2lim[0], end=y2lim[1])}
    p.add_layout(LinearAxis(y_range_name="y2",
                            axis_label=ldict['y2label']), 'right')

    # Hack! But it works. Need to do this *before* you create cds below!
    ix, iy = makePatches(r, y1lim)

    # The "master" data source to be used for plotting.
    #    I wish there was a way of abstracting this but I'm not *quite*
    #    clever enough with a baby imminent. Make the dict in a loop using
    #    the data keys? I dunno. "Future Work" for sure.
    mds = dict(index=r.index, AirTemp=r.AirTemp, Humidity=r.Humidity,
               DewPoint=r.DewPoint, MountTemp=r2.MountTemp,
               ix=ix, iy=iy)
    cds = ColumnDataSource(mds)

    # Make the plots/lines!
    l1, _ = plotLineWithPoints(p, cds, "AirTemp", cwheel[0])
    l2, _ = plotLineWithPoints(p, cds, "DewPoint", cwheel[1])
    l3, _ = plotLineWithPoints(p, cds, "Humidity", cwheel[2], yrname="y2")
    l4, _ = plotLineWithPoints(p, cds, "MountTemp", cwheel[3])

    li1 = LegendItem(label="AirTemp", renderers=[l1])
    li2 = LegendItem(label="DewPoint", renderers=[l2])
    li3 = LegendItem(label="Humidity", renderers=[l3])
    li4 = LegendItem(label="MountTemp", renderers=[l4])
    legend = Legend(items=[li1, li2, li3, li4], location='top_left',
                    orientation='horizontal', spacing=15)
    p.add_layout(legend)

    # HACK HACK HACK HACK HACK
    #   Apply the patches to carry the tooltips
    simg = p.patches('ix', 'iy', source=cds,
                     fill_color=None,
                     fill_alpha=0.0,
                     line_color=None)

    # Make the hovertool only follow the patches (still a hack)
    htline = simg

    # Customize the active tools
    p.toolbar.autohide = True

    ht = HoverTool()
    ht.tooltips = [("Time", "@index{%F %T}"),
                   ("AirTemp", "@AirTemp{0.0} C"),
                   ("MountTemp", "@MountTemp{0.0} C"),
                   ("Humidity", "@Humidity %"),
                   ("DewPoint", "@DewPoint{0.0} C"),
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
