#!/usr/bin/env python

#
# Get the system environment
#
import os
import getopt

#
# Class must match the filename
#
class bb_set:

    def __init__(self, **kwds):

        self.result      = {}
        self.name        = 'set'
        self.description = 'display bb runtime environment'

    #
    # A single call which will return an array passed back via rpcxml
    #
    def bbcall(self, *kwds):

        #
        # Array for the return trip
        #
        ret = []

        #
        # Args (if any)
        #
        if len(kwds[0]) > 0:

            args = kwds[0]

            try:

                opts, args = getopt.getopt(args, "e:s:", ["envvar=","set="])

                for o, a in opts:

                    if o in ("-e", "--envvar"):

                        ret.append(a + " = " + os.environ[a])

                    if o in ("-s", "--set"):

                        ret.append("got = " + a)

            except:

                return self.usage()

        else:

            for env in os.environ:

                ret.append(env + " = " + os.environ[env])

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
        set [ -e var ]
""")

        return ret

#
# Individual test case
#
def bbtest():

    test = bb_set()

    for val in test.bbcall('-e', 'PATH'):

        print val

    for val in test.help():

        print val

#
# If the python file is run via the command line,  bbtest will be called
#
if __name__ == '__main__':

    bbtest()
