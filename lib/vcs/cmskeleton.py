#
# This is a skeleton file for adding additional cm support for bb
#
# Change class bb_cmsystem to bb_<name of cm system>.  Save the 
# file as bb_<name of cm system>.py then restart bb.
#

#
# Any cm system must have the same calls *not* specified with underscores
#

class bb_example:

    #
    # Initialize the class
    #
    def __init__(self, **kwds):

        self.result      = {}
        self.name        = 'example'
        self.description = 'example support for buildbanger'

    #
    # Initial checkout of a source tree
    #
    def initialcheckout(self, *kwds):

    #
    # Checkout files to stdout
    #
    def stdoutupdate(self, *kwds):

    #
    # Return the initial unique hash for source directory
    #
    def initchangenumber(self, *kwds)

    #
    # Return the unique hash for source directory after an update
    #
    def realchangenumber(self, *kwds)

    #
    # Checkout files
    #
    def update(self, *kwds):

    #
    # Get the client specification
    #
    def client(self, *kwds):

    #
    # Get the cm port
    #
    def clientport(self, *kwds):

    #
    # Format the client string for the specific cm system
    #
    def formatclientstring(self, *kwds):

    #
    # Format url used for browsing sources for the specified cm system
    #
    def formaturl(self, *kwds):

    #
    # Return the list of all users with accounts for the specified cm system
    #
    def allusers(self, *kwds):

    #
    # Return an individual user's email address
    #
    def useraddress(self, *kwds):

    #
    # Format list of pending files for use with source browser
    #
    def format_pending(self, *kwds):

    #
    # Get the changes that last affected a build
    #
    def lastcheckout(self, *kwds):

    #
    # Write list of changes back to the database
    #
    def logfilelist(self, *kwds):
