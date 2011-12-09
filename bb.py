#!/usr/bin/env python

#
# buildbanger cli 
#
import os
import sys
import getopt
import xmlrpclib

from sys import stderr

def main():

    global g_force
    global g_server
    global g_command
    global g_port

    file = sys.argv.pop(0)

    try:

        port = os.environ['BBSERVER']

    except:

        print "missing port specification for buildbanger"
        exit(1)

    (g_server, g_port) = port.split(':')

    proxy = xmlrpclib.ServerProxy('http://' + g_server + ":" + g_port)

    proxy._ServerProxy__verbose = 0

    try:

        command = sys.argv.pop(0)

        # print dir(proxy)

        ret = proxy.broker(command, sys.argv)

        for line in ret:

            print line

    except Exception, e:

        print "Exception:", e
        sys.exit(1)


if __name__ == "__main__":

    main()
