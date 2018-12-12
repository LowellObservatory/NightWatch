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

import configparser as conf

import numpy as np
import pandas as pd
from influxdb import DataFrameClient
from influxdb.exceptions import InfluxDBClientError

from ligmos import utils

import mplPlot as mplplot
import bokehPlot as bplot


def parseConfFile(filename):
    """
    """
    try:
        config = conf.SafeConfigParser()
        config.read_file(open(filename, 'r'))
    except IOError as err:
        config = None
        print(str(err))
        return config

    sections = config.sections()
    tsections = ' '.join(sections)

    print("Found the following sections in the configuration file:")
    print("%s\n" % tsections)

    return config


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
        tv = dbinfo['tagv'].split(',')

        # Cleanup
        tv = [each.strip() for each in tv]
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


def getInstTempsDataFrame(host, querystr, port=8086,
                          dbuser='rand', dbpass='pass',
                          dbname='DBname'):
    """
    """
    print(querystr)

    idfc = DataFrameClient(host, port, dbuser, dbpass, dbname)

    # results = idfc.query(q1)
    results = idfc.query(querystr)

    betterResults = {}
    betterCols = {}
    # results is a dict of dataframes, but it's a goddamn mess. Clean it up.
    for rkey in results.keys():
        # rkey is now a tuple of the metric name and the tag + value pair
        #
        # Someone tell me again why Pandas is so great?
        #   I suppose it could be jankiness in influxdb-python?
        #   This magic 'tval' line below is seriously dumb though.
        #
        tval = rkey[1][0][1]
        dat = results[rkey]
        betterResults.update({tval: dat})

    # results = pd.concat(results, axis=1)
    # cols = results.columns.droplevel()

    # This is at least a little better
    return betterResults


if __name__ == '__main__':
    conffile = './dbconn.conf'
    dbconfig = parseConfFile(conffile)

    themefile = "./bokeh_dark_theme.yml"

    # Could easily be looped here
    tdb = dbconfig['insttemps']
    q, flds = queryConstructor(tdb)

    r = getInstTempsDataFrame(tdb['host'], q,
                              port=tdb['port'],
                              dbuser=tdb['user'],
                              dbpass=tdb['pasw'],
                              dbname=tdb['dnme'])

    # Cycle thru the different tag values
    for rkey in r.keys():
        outfile = "./junk_%s.html" % (rkey)

        print("Plotting for %s" % (rkey))
        ptitle = "%s Temperatures" % (rkey)
        figlabels = [ptitle,
                     'Time (UTC)',
                     'CCD Temp (C)',
                     'Aux Temp (C)']

        y1range = [-115, -105]
        y2range = [-10, 30]

        bplot.makeInstTempPlot(r[rkey], outfile, themefile,
                               y1lim=y1range, y2lim=y2range,
                               figlabels=figlabels)
