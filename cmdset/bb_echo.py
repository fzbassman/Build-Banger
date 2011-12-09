#!/usr/bin/env python

#
# Get the system environment
#
import os
import getopt

#
# Class must match the filename
#
class bb_echo:

    def __init__(self, **kwds):

        self.result      = {}
        self.name        = 'echo'
        self.description = 'echo back any string sent as an arg'

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

                opts, args = getopt.getopt(args, "s:", ["string="])

                for o, a in opts:

                    if o in ("-s", "--string"):

                        ret.append(a)

            except:

                return self.usage()

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
        echo -s "string"
""")

        return ret

#
# Individual test case
#
def bbtest():

    test = bb_set()

    for val in test.bbcall('-s', 'echo back string'):

        print val

    for val in test.help():

        print val

#
# If the python file is run via the command line,  bbtest will be called
#
if __name__ == '__main__':

    bbtest()
