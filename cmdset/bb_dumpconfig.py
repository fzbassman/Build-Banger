#!/usr/bin/env python

#
# Get the system environment
#
import os
import getopt
import ConfigParser

config = ConfigParser.RawConfigParser() 

#
# Class must match the filename
#
class bb_dumpconfig:

    def __init__(self, **kwds):

        self.result      = {}
        self.name        = 'dumpconfig'
        self.description = 'dump bb configuration information'

    #
    # A single call which will return an array passed back via rpcxml
    #
    def bbcall(self, *kwds):

        #
        # Array for the return trip
        #
        ret = []

        self.cfgfile = dir + "/conf/bb.cfg"

        config.readfp(open(self.cfgfile))

        for section in config.sections():

            for name, value in config.items(section):

                ret.append(name + " = " + value)

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
        dumpconfig
""")

        return ret

#
# Individual test case
#
def bbtest():

    test = bb_dumpconfig()

    for val in test.bbcall('xx'):

        print val

    for val in test.help():

        print val

#
# If the python file is run via the command line,  bbtest will be called
#
if __name__ == '__main__':

    bbtest()
