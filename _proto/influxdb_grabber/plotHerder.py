# -*- coding: utf-8 -*-
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
#  Created on 21 Dec 2018
#
#  @author: rhamilton

"""
"""

from __future__ import division, print_function, absolute_import

import configparser as conf


class moduleConfig():
    def __init__(self):
        self.title = ''
        self.queries = None
        self.qrange = 1.
        self.pymodule = None

    def assignConf(self, conf):
        pass


class databaseConfig():
    def __init__(self):
        self.host = ''
        self.port = 8086
        self.type = 'influxdb'
        self.tabl = None
        self.user = None
        self.pasw = None


class databaseQuery():
    def __init__(self):
        self.db = None
        self.mn = None
        self.fn = None
        self.dn = None
        self.tn = None
        self.tv = None

    def assignConf(self, conf):
        pass


def parseConfFile(filename, enableCheck=True):
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

    if enableCheck is True:
        enconfig = checkEnabled(config)
    else:
        enconfig = dict(config)

    return enconfig


def checkEnabled(conf):
    """
    """
    enset = {}
    for sect in conf.sections():
        en = False
        for key in conf[sect].keys():
            if key.lower() == 'enabled':
                en = conf[sect].getboolean(key)
                if en is True:
                    enset.update({sect: conf[sect]})

    return enset


def groupConfFiles(queries, modules):
    """
    """
    loopableSet = []
    allQueries = []
    for sect in modules.keys():
        mod = moduleConfig()
        # Loop over all the defined properies in the class that we'll carry
        #   This means that stuff in the conf. files but NOT in the class
        #   will be ignored! Beware.
        for prop in mod.__dict__:
            try:
                setattr(mod, prop, modules[sect][prop])
            except AttributeError:
                print("Attribute %s not found for %s!" % (prop, sect))

        # Now check that the queries defined actually exist and clean
        #   those up into something more usable
        qlist = [each.strip() for each in mod.queries.split(",")]

        # Do this as an explicit loop since we can better warn/scream
        #   Set up each specified database query
        vq = []
        for q in qlist:
            query = databaseQuery()
            for qprop in query.__dict__:
                try:
                    setattr(query, qprop, queries[q][qprop])
                except AttributeError:
                    print("ERROR: %s undefined for query %s!" % (qprop, q))
                    print("Aborting query.")
                    query = None

            if query is None:
                print("Bad query defined! '%s' not found." % (q))
                print("Module %s (%s) is now disabled!" % (mod.title, sect))
                mod = None
                break
            else:
                vq.append(query)

        # Did we survive?
        if mod is not None:
            mod.queries = qlist
            loopableSet.append(mod)
            allQueries += vq


    return loopableSet, set(allQueries)


if __name__ == "__main__":
    qconff = 'dbqueries.conf'
    mconff = 'modules.conf'

    # Parse the text file
    qs = parseConfFile(qconff, enableCheck=False)

    # Now associate the database connection info with each query so it can
    #   be more easily looped and itterated
    # qs = alignDBConfig(qs)

    # Parse the text file and check if any sections are disabled
    ms = parseConfFile(mconff, enableCheck=True)

    # Associate the database queries with the module definitions
    modules, queries = groupConfFiles(qs, ms)

    # 'modules' is now a list of moduleConfig objects. If any of the entries
    #   in mconff had queries that didn't match entries in qconff, that module
    #   was obliterated completely and will be ignored!
    # 'queries' is a list of all the active database sections associated
    #   with the individual modules. It's technically a set, so no dupes.
    print(modules)
    print([q.mn for q in queries])
