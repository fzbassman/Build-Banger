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

hostname = socket.gethostname()
queries  = bbQueries()
db       = bbDatabase()
errors   = bbErrors()
common   = Common()

#
# Class must match the filename
#
class bb_getport:

    def __init__(self, **kwds):

        self.result      = {}
        self.name        = 'getport'
        self.description = 'display sccs port used by a named job'

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

            #
            # Args will *always* end up in the first element due to the way
            # the broker works
            #
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
                        # Call the common routine
                        #
                        port = common.getport(jobname)

                        # 
                        # There needs to be at least one record
                        #
                        if not len(port):

                            #
                            # Format a standard error message
                            #
                            error = errors.formatmsg(1, (jobname, hostname))

                            # 
                            # Append error message to the return array
                            #
                            ret.append(error)

                        else:

                            #
                            # Return the first entry in the array
                            #
                            ret.append(port)

            #
            # Display usage message if an exception is caught
            #
            except:

                ret = self.usage()

        #
        # There was no arg sent, return usage message
        #
        else:

            ret = self.usage()

        #
        # Return whatever is in the arrat
        #
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
        getport -n jobname
""")

        return ret

#
# Individual test case
#
def bbtest():

    test = bb_getport()

    for val in test.bbcall('-n', 'firehose'):

        print val

    for val in test.help():

        print val

#
# If the python file is run via the command line,  bbtest will be called
#
if __name__ == '__main__':

    bbtest()
