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
from bokeh.models import Plot, Range1d, LinearAxis, HoverTool, CrosshairTool,\
                         CustomJSHover
from bokeh.models.formatters import DatetimeTickFormatter
from bokeh.plotting import figure, output_file, save, ColumnDataSource


def makeInstTempPlot(r, outfile, themefile,
                     figlabels=None, y1lim=None, y2lim=None):
    """
    """
    output_file(outfile)
    theme = Theme(filename=themefile)
    tools = "pan, wheel_zoom, box_zoom, crosshair, hover, reset"

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

    if y1lim is None:
        y1lim = [-115, -105]
    p.y_range = Range1d(start=y1lim[0], end=y1lim[1])

    if y2lim is None:
        y2lim = [-10, 30]
    p.extra_y_ranges = {"externalTemps": Range1d(start=y2lim[0], end=y2lim[1])}

    p.add_layout(LinearAxis(y_range_name="externalTemps",
                            axis_label=y2label), 'right')

    # The "master" data source to be used for plotting
    #   INCLUDES a STUPID HACK for better tooltips
    #                THIS IS SO STUPID
    ix = r.index.values
    iy = [np.average(y2lim)*1.5]*len(ix)

    mds = dict(index=r.index, T1=r.T1, T2=r.T2, ix=ix, iy=iy)

    cds = ColumnDataSource(mds)

    l1 = p.line('index', "T1", line_width=2, source=cds,
                color=cwheel[0], legend="Temp1", name="T1")

    l2 = p.line('index', "T2", line_width=2, source=cds,
                y_range_name="externalTemps",
                color=cwheel[1], legend="Temp2", name="T2")

    simg = p.line("ix", "iy", source=cds,
                  y_range_name="externalTemps",
                  color="red", legend="HACK", name="HACK")

    # Make the hovertool only follow this line (bit of a hack)
    htline = simg

    # Customize the active tools
    p.toolbar.autohide = True

    ht = p.select(dict(type=HoverTool))
    # ht.tooltips = [("Time", "@dx{%F %T}"),
    #                ("T1", "@T1"),
    #                ("T2", "@T2")]
    ht.tooltips = [("Time", "@index{%F %T}"),
                   ("T1", "@T1"),
                   ("T2", "@T2")]

    ht.formatters = {'index': 'datetime'}
    ht.show_arrow = False
    # ht.anchor = 'center'
    # ht.attachment = 'above'
    ht.line_policy = 'nearest'
    # ht.attachment = 'vertical'
    ht.renderers = [htline]
    ht.mode = 'vline'

    # Actually apply the theme to the panel
    curdoc().theme = theme
    save(p)

    print("Bokeh plot saved")
