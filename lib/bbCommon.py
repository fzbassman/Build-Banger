#!/usr/bin/env python

#
# Common routines used by other common commands
#

import imp
import socket
import lib.vcs

from lib.bbQueries  import bbQueries
from lib.bbDatabase import bbDatabase

hostname = socket.gethostname()

db      = bbDatabase()
queries = bbQueries()

class Common:

    def __init__(self, **kwds):

        self.description = 'common methods used by multiple classes'
        self.major       = 0
        self.minor       = 1

    def getport(self, jobname):

        port = db.sql_query(queries.returnformatted(6, (hostname, jobname)))

        return port[0][0]

    def getvcs(self, jobname):

        sccs = db.sql_query(queries.returnformatted(7, (hostname, jobname)))

        return sccs[0][0]

    def vcsobject(self, vcs):

        try:

            info_vcs   = imp.find_module(vcs, lib.vcs.__path__)
            module_vcs = imp.load_module(vcs, *info_vcs) 
            vcs_class  = module_vcs.VCS
            vcs_obj    = vcs_class()

        except ImportError:

            print "unable to instantiate " + vcs + " vcs", PyErr_Print()
            return

        return vcs_obj
