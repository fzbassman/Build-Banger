#!/usr/bin/env python

#
# Get the system environment
#
import os
import getopt

#
# Class must match the filename
#
class bb_sysinfo:

    def __init__(self, **kwds):

        self.result      = {}
        self.name        = 'sysinfo'
        self.description = 'show buildbanger server system information'

    #
    # A single call which will return an array passed back via rpcxml
    #
    def bbcall(self, *kwds):

        #
        # Array for the return trip
        #
        ret  = []
        info = []

        uname = os.uname()

        #
        # Args (if any)
        #
        if len(kwds[0]) > 0:

            args = kwds[0]

            try:

                opts, args = getopt.getopt(args, "snrvm", 
                    ["sysname","nodename","release","version","machine"])

            except getopt.GetoptError, err:

                print str(err)
                return self.usage()

            for o, a in opts:

                if o in ("-s", "--sysname"):

                    info.append(uname[0])

                if o in ("-n", "--nodename"):

                    info.append(uname[1])

                if o in ("-r", "--release"):

                    info.append(uname[2])

                if o in ("-v", "--version"):

                    info.append(uname[3])

                if o in ("-m", "--machine"):

                    info.append(uname[4])

            temp = " ".join([str(x) for x in info])
            ret.append(temp);

        else:

            uname = " ".join([str(x) for x in os.uname()])
            ret.append(uname);

        return ret

    #
    # Required help message
    #
    def help(self):

        ret = " %-12s %-s" % (self.name, self.description)

        return ret

    #
    # Required usage message
    #
    def usage(self):

        ret = []

        ret.append("""
Usage:
        sysinfo [-s -n -r -v -m]
""")

        return ret

#
# Individual test case
#
def bbtest():

    test = bb_sysinfo()

    for val in test.bbcall():

        print val

    for val in test.help():

        print val

#
# If the python file is run via the command line,  bbtest will be called
#
if __name__ == '__main__':

    bbtest()
