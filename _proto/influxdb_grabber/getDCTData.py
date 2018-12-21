# -*- coding: utf-8 -*-
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
#  Created on 6 Nov 2018
#
#  @author: rhamilton

"""One line description of module.

Further description.
"""

from __future__ import division, print_function, absolute_import

import numpy as np
import pandas as pd
from influxdb import DataFrameClient
from influxdb.exceptions import InfluxDBClientError

from ligmos import utils

import bokehPlot as bplot
import colorWheelies as cwheels


def queryConstructor(dbinfo, dtime=48):
    """
    dtime is time from present (in hours) to query back

    Allows grouping of the results by a SINGLE tag with multiple values.
    No checking if you want all values for a given tag, so be explicit for now.
    """
    if dbinfo['type'].lower() == 'influxdb':
        print("Constructing influxdb query...")
        print("Searching for %s in %s.%s on %s:%s" % (dbinfo['flds'],
                                                      dbinfo['dnme'],
                                                      dbinfo['mnme'],
                                                      dbinfo['host'],
                                                      dbinfo['port']))

        # Split up the fields into something iterable
        f = dbinfo['flds'].split(',')

        # Same for tags, if any
        tn = dbinfo['tagn'].strip()
        if tn.lower() == "none":
            tn = None
            tv = []
        if tn is not None:
            tv = dbinfo['tagv'].split(',')
            # Cleanup a little more
            tv = [each.strip() for each in tv]

        # Final cleanup
        f = [each.strip() for each in f]

        # TODO: Someone should write a query validator to make sure
        #   this can't run amok.  For now, make sure the user has
        #   only READ ONLY privileges to the database in question!!!
        print("")
        query = 'SELECT'
        for i, each in enumerate(f):
            query += ' "%s"' % (each.strip())
            if i != len(f)-1:
                query += ','
            else:
                query += ' '

        query += 'FROM "%s"' % (dbinfo['mnme'])
        query += ' WHERE time > now() - %02dh' % (dtime)

        if tv != []:
            query += ' AND ('
            for i, each in enumerate(tv):
                query += '"%s"=\'%s\'' % (tn, each.strip())

                if i != len(tv)-1:
                    query += ' OR '
            query += ') GROUP BY "%s"' % (tn)

        return query, f


def getResultsDataFrame(host, querystr, port=8086,
                        dbuser='rand', dbpass='pass',
                        dbname='DBname'):
    """
    Attempts to distinguish queries that have results grouped by a tag
    vs. those which are just of multiple fields. May be buggy still.
    """
    print(querystr)

    idfc = DataFrameClient(host, port, dbuser, dbpass, dbname)

    results = idfc.query(querystr)

    betterResults = {}
    # results is a dict of dataframes, but it's a goddamn mess. Clean it up.
    for rkey in results.keys():
        # If you had a tag that you "GROUP BY" in the query, you'll now have
        #   a tuple of the metric name and the tag + value pair. If you had
        #   no tag to group by, you'll have just the flat result.
        if isinstance(rkey, tuple):
            # Someone tell me again why Pandas is so great?
            #   I suppose it could be jankiness in influxdb-python?
            #   This magic 'tval' line below is seriously dumb though.
            tval = rkey[1][0][1]
            dat = results[rkey]
            betterResults.update({tval: dat})
        elif isinstance(rkey, str):
            betterResults = results[rkey]

    # This is at least a little better
    return betterResults


if __name__ == '__main__':
    conffile = './dbconn.conf'
    dbconfig = parseConfFile(conffile)
    qrange = 36

    themefile = "./bokeh_dark_theme.yml"

    dset, sset = cwheels.getColors()

    # Could easily be looped here
    tdb = dbconfig['insttemps']
    tq, flds = queryConstructor(tdb, dtime=qrange)

    td = getResultsDataFrame(tdb['host'], tq,
                             port=tdb['port'],
                             dbuser=tdb['user'],
                             dbpass=tdb['pasw'],
                             dbname=tdb['dnme'])

    # Cycle thru the different tag values
    for key in td.keys():
        outfile = "./junk_%s.html" % (key)

        print("Plotting for %s" % (key))
        ptitle = "%s Temperatures" % (key)
        figlabels = [ptitle,
                     'Time (UTC)',
                     'CCD Temp',
                     'Aux Temp']

        if key == "deveny":
            y1range = [-115, -105]
            y2range = [-10, 30]
        if key == "lemi":
            y1range = [-125, -115]
            y2range = [-10, 40]

        bplot.makeInstTempPlot(td[key], outfile, themefile, dset,
                               y1lim=y1range, y2lim=y2range,
                               figlabels=figlabels)

    wdb = dbconfig['weather']
    wq, wflds = queryConstructor(wdb, dtime=qrange)
    wd = getResultsDataFrame(wdb['host'], wq,
                             port=wdb['port'],
                             dbuser=wdb['user'],
                             dbpass=wdb['pasw'],
                             dbname=wdb['dnme'])

    outfile = "./junk_weather.html"
    y1range = [-15, 15]
    y2range = [0, 100]
    figlabels = ["WRS Weather Information",
                 'Time (UTC)',
                 'Temperature (C)',
                 'Humidity (%)']
    bplot.makeWeatherPlots(wd, outfile, themefile, dset,
                           y1lim=y1range, y2lim=y2range,
                           figlabels=figlabels)
    print()
