#!/usr/bin/env python

#
# This is the bb plugin class for perforce functionality
#

#
# Any cm system must have the same calls *not* specified with underscores
#

#
# Import required modules
#
import os, sys
import getopt
import socket
import lib.vcs

from lib.bbDatabase import *
from lib.bbQueries  import *

hostname = socket.gethostname()

#
# This class requires the P4 API for Python
#
from P4 import P4, P4Exception

class VCS(lib.vcs.VCS_base):

    #
    # Initialize the class
    #
    def __init__(self, **kwds):

        self.name        = 'perforce'
        self.description = 'perforce support for buildbanger'

        self.result      = {}
        self.P4          = P4()
        self.db          = bbDatabase()
        self.queries     = bbQueries()

    #
    # Initial checkout of a source tree
    #
    def initialcheckout(self, *kwds):

        #
        # Usage message for stdoutupdate
        #
        __usage__ = """\ninitialcheckout usage:\n\n\t-n [--name=] <jobname>\n"""

        #
        # Error flag
        #
        error     = 0

        P4 = self.P4

        #
        # Read args sent in via command line
        #
        if len(kwds) > 0:

            args = kwds[0:]

            #
            # Try/catch, read in -n or display usage message
            #
            try:

                #
                # Read in valid args
                #
                opts, args = getopt.getopt(args, "n:", ["name="])

                #
                # Assign the jobname from the arglist
                #
                for o, a in opts:

                    jobname = a

            #
            # Args were invalid
            #
            except:

                error = 1

        #
        # There were no args sent
        #
        else:

            error = 1

        #
        # This is a usage issue, display usage message
        #
        if error:

            print __usage__
            return

        #
        # Query for certain job parameters
        #
        query = self.queries.returnformatted(8, (hostname, jobname, self.name))
        rows  = self.db.sql_query(query)

        #
        # Make sure the array is populated
        #
        if len(rows):

            for r in rows:

                top      = r[0]
                hostport = r[1]
                client   = r[2]

        else:

            return

        try:

            self.P4.connect()
            self.P4.exception_level = 1

        except P4Exception:

            for e in self.P4.errors:

                print e

        self.P4.disconnect()
        self.P4.connect()

        clientdict = self.P4.run('clients')

        bclient = 0

        for c in clientdict:

            if c['client'] == client:

                bclient = 1
                break

    #
    # Checkout files to stdout
    #
    def stdoutupdate(self, *kwds):

        #
        # Usage message for stdoutupdate
        #
        __usage__ = """\nstdoutupdate usage:\n\n\t-n [--name=] <jobname>\n"""

        #
        # Error flag
        #
        error     = 0

        ret = []

        #
        # Read args sent in via command line
        #
        if len(kwds) > 0:

            args = kwds[0:]

            #
            # Try/catch, read in -n or display usage message
            #
            try:

                #
                # Read in valid args
                #
                opts, args = getopt.getopt(args, "n:", ["name="])

                #
                # Assign the jobname from the arglist
                #
                for o, a in opts:

                    jobname = a

            #
            # Args were invalid
            #
            except:

                error = 1

        #
        # There were no args sent
        #
        else:

            error = 1

        #
        # This is a usage issue, display usage message
        #
        if error:

            print __usage__
            return

        #
        # Query for certain job parameters
        #
        query = self.queries.returnformatted(8, (hostname, jobname, self.name))
        rows  = self.db.sql_query(query)

        #
        # Make sure the array is populated
        #
        if len(rows):

            for r in rows:

                top    = r[0]
                port   = r[1]
                client = r[2]

        else:

            return

        ret.append('VCS perforce stdoutupdate')
        return ret

        if os.path.exists(top) == False:

            self.initialcheckout('-n', jobname)
            return

    #
    # Return the initial unique hash for source directory
    #
    def initchangenumber(self, *kwds):

        #
        # Read args sent in via command line
        #
        if len(kwds) > 0:

            args = kwds[0:]

            #
            # Try/catch, read in -n or display usage message
            #
            try:

                #
                # Read in valid args
                #
                opts, args = getopt.getopt(args, "n:", ["name="])

                #
                # Assign the jobname from the arglist
                #
                for o, a in opts:

                    jobname = a

            #
            # Args were invalid
            #
            except:

                error = 1

    #
    # Return the unique hash for source directory after an update
    #
    def realchangenumber(self, *kwds):

        print "todo"

    #
    # Checkout files
    #
    def update(self, *kwds):

        print "todo"

    #
    # Get the client specification
    #
    def client(self, *kwds):

        print "todo"

    #
    # Get the cm port
    #
    def clientport(self, *kwds):

        print "todo"

    #
    # Format the client string for the specific cm system
    #
    def formatclientstring(self, *kwds):

        print "todo"

    #
    # Format url used for browsing sources for the specified cm system
    #
    def formaturl(self, *kwds):

        print "todo"

    #
    # Return the list of all users with accounts for the specified cm system
    #
    def allusers(self, *kwds):

        print "todo"

    #
    # Return an individual user's email address
    #
    def useraddress(self, *kwds):

        print "todo"

    #
    # Format list of pending files for use with source browser
    #
    def format_pending(self, *kwds):

        print "todo"

    #
    # Get the changes that last affected a build
    #
    def lastcheckout(self, *kwds):

        print "todo"

    #
    # Write list of changes back to the database
    #
    def logfilelist(self, *kwds):

        print "todo"

#
# Individual test case
#
def bbtest():

    test = bb_perforce()

    id          = 'perforce'
    constructor = globals()[id]
    instance    = constructor()

    #
    # This will display the job name
    #
    instance.stdoutupdate('-n', 'profile_trunk')

#
# If the python file is run via the command line,  bbtest will be called
#
if __name__ == '__main__':

    bbtest()
