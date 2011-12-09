#!/usr/bin/env python

#
# Get the system environment
#
import os
import sys
import imp
import getopt
import socket
import lib.vcs

dir      = os.getcwd()
lib_path = os.path.abspath(dir)

sys.path.append(lib_path);

from lib.bbQueries   import bbQueries
from lib.bbDatabase  import bbDatabase
from lib.bbErrors    import bbErrors
from lib.bbCommon    import Common

hostname  = socket.gethostname()

db        = bbDatabase()
queries   = bbQueries()
errors    = bbErrors()
common    = Common()

#
# Class must match the filename
#
class bb_nextjob:

    def __init__(self, **kwds):

        self.result      = {}
        self.name        = 'nextjob'
        self.description = 'display pending changes for <jobname>'

    #
    # A single call which will return an array passed back via rpcxml
    #
    def bbcall(self, *kwds):

        #
        # Array for the return trip
        #
        ret = []

        jobname = ''

        #
        # Args (if any)
        #
        if len(kwds[0]) > 0:

            args = kwds[0]

            try:

                #
                # Get required args for this method
                #
                opts, args = getopt.getopt(args, "n:", ["name="])

                #
                # Iterate through the args
                #
                for o, a in opts:

                    if o in ("-n", "--name"):

                        #
                        # Assign the arg to jobname
                        #
                        jobname = a

                        #
                        # Create the query
                        #
                        query = queries.returnformatted(5, (hostname, jobname))

                        #
                        # Query the database
                        #
                        ret = db.sql_query(query)

                        #
                        # Get the port and vcs used for this job
                        #
                        port = common.getport(jobname)
                        vcs  = common.getvcs(jobname)

                        # 
                        # There needs to be at least one record
                        #
                        if not len(ret):

                            error = errors.formatmsg(1, (jobname, hostname))
                            ret.append(error)

            except:

                ret = self.usage()

        else:

            ret = self.usage()

        vcs_obj    = common.vcsobject(vcs)
        ret        = vcs_obj.stdoutupdate('-n', jobname)

        return ret

    #
    # Required help message
    #
    def help(self):

        ret = " %-12s %s" % (self.name, self.description)

        return ret

    #
    # Required usage message
    #
    def usage(self):

        ret = []

        ret.append("""
Usage:
        nextjob -n jobname
""")

        return ret

#
# Individual test case
#
def bbtest():

    test = bb_nextjob()

    for val in test.bbcall('-n', 'profile_trunk'):

        print val

    for val in test.help():

        print val

#
# If the python file is run via the command line,  bbtest will be called
#
if __name__ == '__main__':

    bbtest()
