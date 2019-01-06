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

from collections import OrderedDict

import numpy as np
import datetime as dt

from bokeh.themes import Theme
from bokeh.layouts import widgetbox
from bokeh.io import curdoc, output_file, show
from bokeh.models import Plot, Range1d, LinearAxis, DatetimeAxis, \
    HoverTool, CrosshairTool, CustomJSHover, Quad, Legend, LegendItem, \
    DataTable, TableColumn
from bokeh.models.formatters import DatetimeTickFormatter
from bokeh.plotting import figure, output_file, save, ColumnDataSource


class valJudgement(object):
    def __init__(self):
        self.label = None
        self.value = None
        self.timestamp = None
        self.tooOld = False

    def judgeAge(self, maxage=None,
                 comptime=None):
        # Need to put everything into Numpy datetime64/timedelta64 objects
        #   to allow easier interoperations
        if maxage is None:
            maxage = dt.timedelta(minutes=5.5)
            maxage = np.timedelta64(maxage)

        if comptime is None:
            comptime = np.datetime64(dt.datetime.utcnow())

        delta = comptime - self.timestamp
        if delta > maxage:
            self.tooOld = True
        else:
            self.tooOld = False


def getLast(p1, lastIdx=None, comptime=None):
    """
    """
    if lastIdx is None:
        # Get the last valid position/value in the dataframe
        lastIdx = p1.last_valid_index()

    retObj = valJudgement()
    retObj.label = p1.name
    retObj.value = p1[lastIdx]

    # Use datetime64 to avoid an annoying nanoseconds warning when
    #   using just regular .to_pydatetime()
    retObj.timestamp = lastIdx.to_datetime64()
    retObj.judgeAge(comptime=comptime)

    return retObj


def deshred(plist, delim=":", name=None, lastIdx=None,
            comptime=None, last=True):
    """
    NOTE: p1 thru 3 are expected to be Pandas dataframes
    """
    if comptime is None:
        comptime = np.datetime64(dt.datetime.utcnow())

    if last is True:
        retStr = ""
        for i, each in enumerate(plist):
            # Made this a function so I can reuse it elsewhere
            retVal = getLast(each, lastIdx=lastIdx)

            # Smoosh it all together; if it's the last value, don't
            #   add the delim since it's not needed at the end of the str
            if i == len(plist) - 1:
                delim = ""

            try:
                retStr += "%02d%s" % (retVal.value, delim)
            except TypeError:
                # This means we probably had heterogeneous datatypes so just
                #   print them all as strings to move on quickly
                retStr += "%s%s" % (retVal.value, delim)

        # Pack everything up for returning it all as one object
        fObj = valJudgement()
        if name is None:
            fObj.label = retVal.label
        else:
            fObj.label = name
        fObj.value = retStr
        fObj.timestamp = retVal.timestamp
        fObj.judgeAge(comptime=comptime)

        return fObj
    else:
        # Should do a sort of a zip dance here to combine the multiple
        #   dataframes into a single dataframe with the delim; would save some
        #   CPU cycles if I did this just after the query so the plotting
        #   routine doesn't have to do it, but that sounds a lot like
        #   "Version 2.0" sort of talk.
        raise NotImplementedError


def checkForEmptyData(indat):
    """
    """
    # Check to make sure we actually have data ...
    abort = False
    for q in indat:
        if len(indat[q]) == 0:
            abort = True
            break

    return abort


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


def assembleFacSumTCS(indat):
    """
    """
    # Common "now" time to compare everything against
    now = np.datetime64(dt.datetime.utcnow())

    # Now the tedious bit - reassemble the shredded parameters like RA/Dec/etc.
    #   Whomever designed the TCS XML...know that I'm not a fan of your work.
    #
    # 'deshred' will automatically take the last entry and return a
    #   non-annoying version with its timestamp for later display.
    #
    # First, get the last valid index in the q_tcssv dataframe and use that
    #   for all the TCS queries to make sure it's at least consistent
    tcsLastIdx = indat['q_tcssv'].cRA_h.last_valid_index()

    # CURRENT coords
    cRA = deshred([indat['q_tcssv'].cRA_h,
                  indat['q_tcssv'].cRA_m,
                  indat['q_tcssv'].cRA_s], delim=":", lastIdx=tcsLastIdx,
                  name="cRA", comptime=now)
    cDec = deshred([indat['q_tcssv'].cDec_d,
                   indat['q_tcssv'].cDec_m,
                   indat['q_tcssv'].cDec_s], delim=":", lastIdx=tcsLastIdx,
                   name="cDec", comptime=now)
    cEpoch = deshred([indat['q_tcssv'].cEqP,
                     indat['q_tcssv'].cEqY,
                     indat['q_tcssv'].cFrame], delim="", lastIdx=tcsLastIdx,
                     name="cEpoch", comptime=now)
    # DEMAND coords
    dRA = deshred([indat['q_tcssv'].dRA_h,
                  indat['q_tcssv'].dRA_m,
                  indat['q_tcssv'].dRA_s], delim=":", lastIdx=tcsLastIdx,
                  name="dRA", comptime=now)
    dDec = deshred([indat['q_tcssv'].dDec_d,
                   indat['q_tcssv'].dDec_m,
                   indat['q_tcssv'].dDec_s], delim=":", lastIdx=tcsLastIdx,
                   name="dDec", comptime=now)
    dEpoch = deshred([indat['q_tcssv'].dEqP,
                     indat['q_tcssv'].dEqY,
                     indat['q_tcssv'].dFrame], delim="", lastIdx=tcsLastIdx,
                     name="dEpoch", comptime=now)

    airmass = getLast(indat['q_tcssv'].Airmass, lastIdx=tcsLastIdx,
                      comptime=now)
    targname = getLast(indat['q_tcssv'].TargetName, lastIdx=tcsLastIdx,
                       comptime=now)
    guidemode = getLast(indat['q_tcssv'].GuideMode, lastIdx=tcsLastIdx,
                        comptime=now)
    sundist = getLast(indat['q_tcssv'].SunDistance, lastIdx=tcsLastIdx,
                      comptime=now)
    moondist = getLast(indat['q_tcssv'].MoonDistance, lastIdx=tcsLastIdx,
                       comptime=now)

    # Finally done! Now put it all into a list so it can be passed
    #   back a little easier and taken from there
    tableDat = [now, targname,
                cRA, cDec, cEpoch,
                dRA, dDec, dEpoch,
                airmass, guidemode,
                sundist, moondist]

    values = []
    labels = []
    for i, each in enumerate(tableDat):
        if i == 0:
            values.append(str(each))
            labels.append("LastUpdated")
        else:
            values.append(each.value)
            labels.append(each.label)

    mds = dict(labels=labels, values=values)
    cds = ColumnDataSource(mds)

    return cds


def assembleFacSumLPI(indat):
    """
    """
    # Common "now" time to compare everything against
    now = np.datetime64(dt.datetime.utcnow())

    # Now the tedious bit - reassemble the shredded parameters like RA/Dec/etc.
    #   Whomever designed the TCS XML...know that I'm not a fan of your work.
    #
    # 'deshred' will automatically take the last entry and return a
    #   non-annoying version with its timestamp for later display.
    #
    # First, get the last valid index in the q_tcssv dataframe and use that
    #   for all the TCS queries to make sure it's at least consistent
    tcsLastIdx = indat['q_tcssv'].cRA_h.last_valid_index()

    mirrorcov = getLast(indat['q_tcssv'].MirrorCover, lastIdx=tcsLastIdx,
                        comptime=now)

    # These are from other data sources, so get their values too
    domeshut = getLast(indat['q_tcslois'].DomeShutter, comptime=now)
    instcover = getLast(indat['q_cubeinstcover'].InstCover, comptime=now)

    cubeLastIdx = indat['q_cubefolds'].PortThru.last_valid_index()
    portT = getLast(indat['q_cubefolds'].PortThru, lastIdx=cubeLastIdx,
                    comptime=now)
    portA = getLast(indat['q_cubefolds'].PortA, lastIdx=cubeLastIdx,
                    comptime=now)
    portB = getLast(indat['q_cubefolds'].PortB, lastIdx=cubeLastIdx,
                    comptime=now)
    portC = getLast(indat['q_cubefolds'].PortC, lastIdx=cubeLastIdx,
                    comptime=now)
    portD = getLast(indat['q_cubefolds'].PortD, lastIdx=cubeLastIdx,
                    comptime=now)

    # Finally done! Now put it all into a list so it can be passed
    #   back a little easier and taken from there
    tableDat = [now,
                domeshut, mirrorcov, instcover,
                portT, portA, portB, portC, portD]

    values = []
    labels = []
    for i, each in enumerate(tableDat):
        if i == 0:
            values.append(str(each))
            labels.append("LastUpdated")
        elif each.label == "InstCover":
            # Special conversion to text for this one
            if each.value == 0:
                values.append("Closed")
            else:
                values.append("Open")
            labels.append(each.label)
        elif each.label.startswith("Port"):
            if each.value == 0:
                values.append("Inactive")
            else:
                values.append("Active")
            labels.append(each.label)
        else:
            values.append(each.value)
            labels.append(each.label)

    mds = dict(labels=labels, values=values)
    cds = ColumnDataSource(mds)

    return cds


def makeFacSumLPI(indat, outfile, themefile, cwheel):
    """
    """
    #
    # TODO:
    #   I should *really* think about incorporating this into the other modules
    #
    abort = checkForEmptyData(indat)
    if abort is True:
        print("No data found! Aborting.")
        return None

    cds = assembleFacSumLPI(indat)
    print()

    cols = []
    for c in cds.column_names:
        print(c)
        col = TableColumn(field=c, title=c)
        cols.append(col)

    # Now actually construct the table
    output_file(outfile)
    dtab = DataTable(columns=cols, source=cds)
    show(widgetbox(dtab))


def makeFacSumTCS(indat, outfile, themefile, cwheel):
    """
    """
    #
    # TODO:
    #   I should *really* think about incorporating this into the other modules
    #
    abort = checkForEmptyData(indat)
    if abort is True:
        print("No data found! Aborting.")
        return None

    cds = assembleFacSumTCS(indat)
    print()

    cols = []
    for c in cds.column_names:
        print(c)
        col = TableColumn(field=c, title=c)
        cols.append(col)

    # Now actually construct the table
    output_file(outfile)
    dtab = DataTable(columns=cols, source=cds)
    show(widgetbox(dtab))


def makeWindPlots(indat, outfile, themefile, cwheel):
    """
    """

    y1lim = [0, 15]

    r = indat['q_wrs']
    output_file(outfile)
    theme = Theme(filename=themefile)

    ldict = {'title': "WRS Wind Information",
             'xlabel': "Time (UTC)",
             'y1label': "Wind Speed (m/s)"}

    p = commonPlot(r, ldict)
    timeNow = dt.datetime.utcnow()
    tWindow = dt.timedelta(hours=24)

    if y1lim is None:
        y1lim = [r.WindSpeedMin.values.min,
                 r.WindSpeedMax.values.max]
    p.y_range = Range1d(start=y1lim[0], end=y1lim[1])
    p.x_range = Range1d(start=timeNow-tWindow, end=timeNow)

    # Hack! But it works. Need to do this *before* you create cds below!
    ix, iy = makePatches(r, y1lim)

    # The "master" data source to be used for plotting.
    #    I wish there was a way of abstracting this but I'm not *quite*
    #    clever enough with a baby imminent. Make the dict in a loop using
    #    the data keys? I dunno. "Future Work" for sure.
    mds = dict(index=r.index,
               WindSpeed=r.WindSpeed,
               WindSpeedMin=r.WindSpeedMin,
               WindSpeedMax=r.WindSpeedMax,
               WindDir=r.WindDir,
               ix=ix, iy=iy)
    cds = ColumnDataSource(mds)

    # Make the plots/lines!
    l1, _ = plotLineWithPoints(p, cds, "WindSpeed", cwheel[0])
    l2, _ = plotLineWithPoints(p, cds, "WindSpeedMin", cwheel[1])
    l3, _ = plotLineWithPoints(p, cds, "WindSpeedMax", cwheel[2])

    li1 = LegendItem(label="WindSpeed", renderers=[l1])
    li2 = LegendItem(label="WindSpeedMin", renderers=[l2])
    li3 = LegendItem(label="WindSpeedMax", renderers=[l3])
    legend = Legend(items=[li1, li2, li3], location='top_left',
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
                   ("WindSpeed", "@WindSpeed{0.0} m/s"),
                   ("WindSpeedMin", "@WindSpeedMin{0.0} m/s"),
                   ("WindSpeedMax", "@WindSpeedMax{0.0} m/s")
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
