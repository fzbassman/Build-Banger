#!/usr/bin/env python

#
# This is the bb plugin class for mercurial functionality
#

#
# Any cm system must have the same calls *not* specified with underscores
#

#
# Import required modules
#
import os
import getopt

class bb_mercurial:

    #
    # Initialize the class
    #
    def __init__(self, **kwds):

        self.result      = {}
        self.name        = 'mercurial'
        self.description = 'mercurial support for buildbanger'

    #
    # Initial checkout of a source tree
    #
    def initialcheckout(self, *kwds):

        print "todo"

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
        # Everything worked out...
        #

    #
    # Return the initial unique hash for source directory
    #
    def initchangenumber(self, *kwds):

        print "todo"

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

    test = bb_mercurial()

    test.stdoutupdate('-x', 'fubar')

    test.stdoutupdate('-n', 'fubar')


#
# If the python file is run via the command line,  bbtest will be called
#
if __name__ == '__main__':

    bbtest()
