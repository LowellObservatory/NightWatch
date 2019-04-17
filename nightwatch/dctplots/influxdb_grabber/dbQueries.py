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


def queryConstructor(dbinfo, dtime=48, debug=False):
    """
    dbinfo is type databaseQuery, which includes databaseConfig as
    dbinfo.db.  More info in 'confHerder'.

    dtime is time from present (in hours) to query back

    Allows grouping of the results by a SINGLE tag with multiple values.
    No checking if you want all values for a given tag, so be explicit for now.
    """
    if isinstance(dtime, str):
        try:
            dtime = int(dtime)
        except ValueError:
            print("Can't convert %s to int!" % (dtime))
            dtime = 1

    if dbinfo.db.type.lower() == 'influxdb':
        print("Constructing influxdb query...")
        if debug is False:
            print("Searching for %s in %s.%s on %s:%s" % (dbinfo.fn,
                                                          dbinfo.db.tabl,
                                                          dbinfo.mn,
                                                          dbinfo.db.host,
                                                          dbinfo.db.port))

        # Some renames since this was adapted from an earlier version
        tn = dbinfo.tn
        if tn is not None:
            tv = dbinfo.tv
        else:
            tv = []

        # TODO: Someone should write a query validator to make sure
        #   this can't run amok.  For now, make sure the user has
        #   only READ ONLY privileges to the database in question!!!
        print("")
        query = 'SELECT'
        if isinstance(dbinfo.fn, list):
            for i, each in enumerate(dbinfo.fn):
                # Catch possible fn/dn mismatch
                try:
                    query += ' "%s" AS "%s"' % (each.strip(), dbinfo.dn[i])
                except IndexError:
                    query += ' "%s"' % (each.strip())
                if i != len(dbinfo.fn)-1:
                    query += ','
                else:
                    query += ' '
        else:
            if dbinfo.dn is not None:
                query += ' "%s" AS "%s" ' % (dbinfo.fn, dbinfo.dn)
            else:
                query += ' "%s" ' % (dbinfo.fn)

        query += 'FROM "%s"' % (dbinfo.mn)
        query += ' WHERE time > now() - %02dh' % (dtime)

        if tv != []:
            query += ' AND ('
            if isinstance(dbinfo.tv, list):
                for i, each in enumerate(tv):
                    query += '"%s"=\'%s\'' % (tn, each.strip())

                    if i != len(tv)-1:
                        query += ' OR '
                query += ') GROUP BY "%s"' % (tn)
            else:
                # If we're here, there was only 1 tag value so we don't need
                #   to GROUP BY anything
                query += '"%s"=\'%s\')' % (tn, tv)

        return query


def getResultsDataFrame(host, querystr, port=8086,
                        dbuser='rand', dbpass='pass',
                        dbname='DBname', datanames=None):
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
