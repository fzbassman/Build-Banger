#!/usr/bin/env python

#
# Get the system environment
#
import os
import getopt
import socket

from lib.bbQueries  import bbQueries
from lib.bbDatabase import bbDatabase
from lib.bbErrors   import bbErrors
from lib.bbCommon   import Common

hostname  = socket.gethostname()

queries = bbQueries()
db      = bbDatabase()
errors  = bbErrors()
common  = Common()

#
# Class must match the filename
#
class bb_describe:

    def __init__(self, **kwds):

        self.result      = {}
        self.name        = 'describe'
        self.description = 'describe build job characteristics'

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

                        common.getport(jobname)

                        common.getvcs(jobname)

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
        describe -n jobname
""")

        return ret

#
# Individual test case
#
def bbtest():

    test = bb_set()

    for val in test.bbcall('-n', 'firehose'):

        print val

    for val in test.help():

        print val

#
# If the python file is run via the command line,  bbtest will be called
#
if __name__ == '__main__':

    bbtest()
