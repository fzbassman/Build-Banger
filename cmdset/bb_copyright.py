#!/usr/bin/env python

#
# Get the system environment
#
import os

#
# Class must match the filename
#
class bb_copyright:

    def __init__(self, **kwds):

        self.result      = {}
        self.name        = 'copyright'
        self.description = 'buildbanger copyright information'

    #
    # A single call which will return an array passed back via rpcxml
    #
    def bbcall(self, *kwds):

        #
        # Array for the return trip
        #
        ret = []

        ret.append("buildbanger(c) 1997-2011, eric wallengren")

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
        copyright
""")

        return ret

#
# Individual test case
#
def bbtest():

    test = bb_hello()

    for val in test.bbcall():

        print val

    for val in test.help():

        print val

#
# If the python file is run via the command line,  bbtest will be called
#
if __name__ == '__main__':

    bbtest()
