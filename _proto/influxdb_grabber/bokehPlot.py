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


def makeInstTempPlot(r, outfile, themefile,
                     figlabels=None, y1lim=None, y2lim=None):
    """
    """
    output_file(outfile)
    theme = Theme(filename=themefile)
    tools = "pan, wheel_zoom, box_zoom, crosshair, reset"

    cwheel = ['#7EB26D', '#EAB839']

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

    p.x_range = Range1d(start=r.index[0], end=r.index[-1])

    if y1lim is None:
        y1lim = [-115, -105]
    p.y_range = Range1d(start=y1lim[0], end=y1lim[1])

    if y2lim is None:
        y2lim = [-10, 30]
    p.extra_y_ranges = {"externalTemps": Range1d(start=y2lim[0], end=y2lim[1])}
    p.add_layout(LinearAxis(y_range_name="externalTemps",
                            axis_label=y2label), 'right')

    #   INCLUDES a HACK for better tooltips of turning the indicies
    #   into a list of lists of x coordinate and y coordinate sets
    #   to make a series of adjacent patches.  Their width is the time
    #   between two datapoints and height spans the (initial) y1 range
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

    # The "master" data source to be used for plotting
    mds = dict(index=r.index, T1=r.T1, T2=r.T2, ix=ix, iy=iy)
    cds = ColumnDataSource(mds)

    # NOTE: The way the polling is done, mode='after' is the correct step mode
    #   since I get the result and then sleep for an interval
    l1 = p.step('index', "T1", line_width=1, source=cds, mode='after',
                color=cwheel[0], legend=y1label, name=y1label)
    s1 = p.scatter('index', "T1", size=8, source=cds,
                   color=cwheel[0], legend=y1label, name=y1label,
                   alpha=0., hover_alpha=1., hover_color='#E24D42')

    l2 = p.step('index', "T2", line_width=1, source=cds, mode='before',
                y_range_name="externalTemps",
                color=cwheel[1], legend=y2label, name=y2label)
    s2 = p.scatter('index', "T2", size=8, source=cds,
                   y_range_name="externalTemps",
                   color=cwheel[1], legend=y2label, name=y2label,
                   alpha=0., hover_alpha=1., hover_color='#E24D42')

    # HACK HACK HACK HACK HACK
    #   Make a whole bunch of patches that carry the tooltips
    simg = p.patches('ix', 'iy', source=cds,
                     fill_color="#b3de69",
                     fill_alpha=0.0,
                     line_color=None)

    # Make the hovertool only follow this line (bit of a hack)
    htline = simg

    # Customize the active tools
    p.toolbar.autohide = False

    ht = HoverTool()
    ht.tooltips = [("Time", "@index{%F %T}"),
                   ("T1", "@T1"),
                   ("T2", "@T2")]
    ht.formatters = {'index': 'datetime'}
    ht.show_arrow = False
    ht.point_policy = 'follow_mouse'
    ht.line_policy = 'nearest'
    ht.renderers = [htline]
    p.add_tools(ht)

    # Actually apply the theme to the panel
    curdoc().theme = theme
    save(p)

    print("Bokeh plot saved")
