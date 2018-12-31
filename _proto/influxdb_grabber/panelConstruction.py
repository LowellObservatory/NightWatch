# -*- coding: utf-8 -*-
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
#  Created on 26 Dec 2018
#
#  @author: rhamilton

"""
"""

from __future__ import division, print_function, absolute_import

from collections import OrderedDict

import pandas as pd

import confHerder as ch
import dbQueries as dbq
import modulePlots as bplot
import colorWheelies as cwheels


def main(qconff, mconff, theme='dark'):
    """
    """
    mods, quer = ch.parser(qconff, mconff)
    # 'mods' is a list of ch.moduleConfig objects.
    # 'quer' is a list of all the active database sections associated

    if theme == 'dark':
        themefile = "./bokeh_dark_theme.yml"
    else:
        print("No other themes available yet!")
        print("dark theme it is, then.")
        themefile = "./bokeh_dark_theme.yml"

    # Get the default color sets; second one is sorted by hue but
    #   I'm ditching it since I'm not using it
    dset, _ = cwheels.getColors()

    qdata = OrderedDict()
    for iq in quer.keys():
        q = quer[iq]
        query = dbq.queryConstructor(q, dtime=q.rn)
        td = dbq.getResultsDataFrame(q.db.host, query,
                                     q.db.port,
                                     dbuser=q.db.user,
                                     dbpass=q.db.pasw,
                                     dbname=q.db.tabl,
                                     datanames=q.dn)
        qdata.update({iq: td})

    print("%d queries complete!" % (len(qdata)))

    # Cycle thru each module and generate it
    for m in mods:
        print(m.title)
        # Gather up the query data into a single dict so we don't
        #   have to encode absolutely everything in every single plot/page
        pdata = OrderedDict()
        for qtag in m.queries.keys():
            pdata.update({qtag: qdata[qtag]})

        # A neat party trick:
        #   Grab the actual function reference by getting the named
        #   attribute of an import (bplot). Then we can call
        #   'thingLonger' with the args to actually do it.
        try:
            thingLonger = getattr(bplot, m.pymodule)
        except AttributeError:
            print("FATAL ERROR: Module %s not found!" % (m.pymodule))

        outfile = m.outname
        thingLonger(pdata, outfile, themefile, dset)

    # bplot.makeWeatherPlots(wd, outfile, themefile, dset,

    # print())

    # # Cycle thru the different tag values
    # for key in td.keys():
    #     outfile = "./junk_%s.html" % (key)

    #     print("Plotting for %s" % (key))
    #     ptitle = "%s Temperatures" % (key)
    #     figlabels = [ptitle,
    #                  'Time (UTC)',
    #                  'CCD Temp',
    #                  'Aux Temp']

    #     if key == "deveny":
    #         y1range = [-115, -105]
    #         y2range = [-10, 30]
    #     if key == "lemi":
    #         y1range = [-125, -115]
    #         y2range = [-10, 40]

    #     bplot.makeInstTempPlot(td[key], outfile, themefile, dset,
    #                            y1lim=y1range, y2lim=y2range,
    #                            figlabels=figlabels)

    # wdb = dbconfig['weather']
    # wq, wflds = dbq.queryConstructor(wdb, dtime=qrange)
    # wd = dbq.getResultsDataFrame(wdb['host'], wq,
    #                              port=wdb['port'],
    #                              dbuser=wdb['user'],
    #                              dbpass=wdb['pasw'],
    #                              dbname=wdb['dnme'])


if __name__ == "__main__":
    qconff = 'dbqueries.conf'
    mconff = 'modules.conf'
    main(qconff, mconff)
