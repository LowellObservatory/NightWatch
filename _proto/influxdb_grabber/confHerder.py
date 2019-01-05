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
from collections import OrderedDict


class moduleConfig():
    def __init__(self):
        self.title = ''
        self.queries = None
        self.drange = 1
        self.pymodule = None
        self.outname = None
        self.enabled = False

    def combineConfs(self, queries):
        qdict = OrderedDict()
        # Take care of single query configurations; otherwise the following
        #   loop would shred the string into its component characters and
        #   would obviously not work
        if isinstance(self.queries, str):
            self.queries = [self.queries]

        for q in self.queries:
            try:
                qdict.update({q: queries[q]})
            except KeyError:
                print("Query %s is undefined! Skipping it..." % (q))

        self.queries = qdict


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
        self.rn = 24


def assignConf(obj, conf):
    for key in obj.__dict__:
        try:
            kval = conf[key]
            kval = kval.strip().split(",")
            kval = [kv.strip() for kv in kval]

            # kval is now definitely a list
            nkval = []
            for val in kval:
                if val.lower() == "none":
                    nkval.append(None)
                else:
                    nkval.append(val)

            # If there's just one object then return it flat
            if len(nkval) == 1:
                nkval = nkval[0]
            setattr(obj, key, nkval)
        except KeyError:
            print("Improper config!")
            print("Missing key %s" % (key))
            setattr(obj, key, None)

    return obj


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
    enset = OrderedDict()
    for sect in conf.sections():
        en = False
        for key in conf[sect].keys():
            if key.lower() == 'enabled':
                en = conf[sect].getboolean(key)
                if en is True:
                    enset.update({sect: conf[sect]})

    return enset


def alignDBConfig(queries):
    """
    """
    dbs = OrderedDict()
    vqs = OrderedDict()
    for sec in queries:
        if sec.lower().startswith("database-"):
            idb = assignConf(databaseConfig(), queries[sec])
            dbs.update({sec: idb})
        elif sec.lower() != 'default':
            dbq = assignConf(databaseQuery(), queries[sec])
            dbq.key = sec
            try:
                dbkey = queries[sec]['db']
                dbq.db = dbs[dbkey]
            except AttributeError:
                print("FATAL ERROR: database %s not specified!" % (dbkey))
                dbq = None
            vqs.update({sec: dbq})

    return vqs


def groupConfFiles(queries, modules):
    """
    """
    loopableSet = []
    allQueries = []
    for sect in modules.keys():
        # Parse the conf file section
        mod = assignConf(moduleConfig(), modules[sect])

        # Assign the query objects to the module class now
        mod.combineConfs(queries)

        # Sanity checks
        if mod.queries == {}:
            # This means we didn't find any valid queries so we'll skip
            #   the module entirely so we don't crash out
            mod = None

        # Did we survive?
        if mod is not None:
            loopableSet.append(mod)
            allQueries += mod.queries.values()

        # Turn the unique set of queries into something a little easier to
        #   interact and associate with later on in the codes
        qS = set(allQueries)
        qDict = OrderedDict()
        for q in qS:
            qDict.update({q.key: q})

    return loopableSet, qDict


def parser(qconff, mconff):
    """
    """
    # Parse the text file
    qs = parseConfFile(qconff, enableCheck=False)

    # Associate the database queries with the proper database connection class
    qs = alignDBConfig(qs)

    # Parse the text file and check if any sections are disabled
    ms = parseConfFile(mconff, enableCheck=True)

    # Now combine the moduels and queries into stuff we can itterate over
    modules, queries = groupConfFiles(qs, ms)

    # 'modules' is now a list of moduleConfig objects. If any of the entries
    #   in mconff had queries that didn't match entries in qconff, that module
    #   was obliterated completely and will be ignored!
    # 'queries' is a list of all the active database sections associated
    #   with the individual modules. It's technically a set, so no dupes.
    # Now we're ready for an actual loop! But let someone else do it.

    return modules, queries
