#
# Server functions used for bb
#
import os
import sys
import time
import socket
import xmlrpclib
import subprocess
import ConfigParser

from SimpleXMLRPCServer import SimpleXMLRPCServer
from bbQueries       import bbQueries
from bbDatabase      import bbDatabase
from bbCommands      import *

hostname  = socket.gethostname()
queries   = bbQueries()
db        = bbDatabase()
dir       = os.getcwd()
config    = ConfigParser.RawConfigParser()
commands  = bbCommands()

class bbServer:

    finished=False 

    #
    # Initialize class
    #
    def __init__(self, **kwds):

        self.debug = 1

        self.port = None;

        #
        # Create the database object
        #
        db = bbDatabase()

        #
        # Create database connection
        #
        self.con = db.getbbcon()

        #
        # Create the bb directory structure if it doesn't exist
        #
        self.__createbbdirs()

        #
        # Read or create necessary bb configuration
        #
        self.__readconfigfile()

        #
        # Load all commands
        #
        commands.loadcommands()

        #
        # Assign command object to this class
        #
        self.commands = commands.commands

        #
        # See if port was sent as an arg, assing it
        #
        if kwds.has_key('port'):

            self.port = kwds['port']

        #
        # If port wasn't sent, prompt for it
        #
        while not self.port:

            self.port = raw_input('enter port number for RPC service: ')

        #
        # Start the rpc server
        #
        self.startserver()

        print "server loading completed"

    #
    # Start the RPCXML Server process
    #
    def startserver(self):

        #
        # Start rpcxml service
        #
        self.__loadrpcxml()

    #
    # Register server locally (known by it's own database)
    #
    def registerserver(self):

        #
        # Get uname info
        #
        uname = " ".join([str(x) for x in os.uname()])

        if not self.__serverexists():

            #
            # Generate record array
            #
            #record = (hostname, uname, 9190, 1, 'dev@company.com', 1)
            record = ('0.0.0.0', uname, 9190, 1, 'dev@company.com', 1)
            db.sql_insert('buildservers', record)

        else:

            #
            # See if this server already exists in the table
            #
            query = queries.returnformatted(3, (1, hostname))
            rows = db.sql_query(query)

    #
    # Unregister the server
    #
    def unregisterserver(self):

        #
        # See if this server already exists in the table
        #
        if self.__serverexists():

            #
            # See if this server already exists in the table
            #
            query = queries.returnformatted(3, (0, hostname))
            rows = db.sql_query(query)

    #
    # See if server exists
    #
    def __serverexists(self):

        #
        # See if this server already exists in the table
        #
        query = queries.returnformatted(2, ('buildservers', hostname))
        rows  = db.sql_query(query)

        #
        # If a record was found return true
        #
        if len(rows):
            return True
        else:
            return False

    #
    # Create bb directory structure
    #
    def __createbbdirs(self):

        #
        # If the config files doesn't exist, define vars and create
        # the configuration
        #
        self.srcdir   = dir + "/src"
        self.builddir = dir + "/builds"
        self.promodir = dir + "/promotion"
        self.logdir   = dir + "/logs"

        if not os.path.exists('src'):
            os.mkdir('src')

        if not os.path.exists('builds'):
            os.mkdir('builds')

        if not os.path.exists('promotion'):
            os.mkdir('promotion')

        if not os.path.exists('logs'):
            os.mkdir('logs')

    #
    # Generate config file if necessary
    #
    def __readconfigfile(self):

        """
        Check to see if a configuration file exists, otherwise create it
        """

        self.cfgfile  = dir + "/conf/bb.cfg"

        if not os.path.exists('conf'):
            os.mkdir('conf')

        if not os.path.isfile(self.cfgfile):

            #
            # unless otherwise specified, this will be the master
            #
            config.add_section('Master')

            #
            # Add all the values for the master
            #
            config.set('Master', 'port', '9190')
            config.set('Master', 'email', 'buildmeister@company.com')
            config.set('Master', 'fullname', 'Build Meister')
            config.set('Master', 'srcdir', self.srcdir)
            config.set('Master', 'builddir', self.builddir)
            config.set('Master', 'promodir', self.promodir)

            #
            # Write the configuration
            #
            configfile = open(self.cfgfile, "wb")
            config.write(configfile)

        else:

            #
            # The configuration already exists, read  values in
            #
            config.readfp(open(self.cfgfile))

            #
            # Make sure that master and slave aren't both defined
            #
            if config.has_section('Master') and config.has_section('Slave'):

                print "Invalid configuration file!"
                sys.exit(1);

            #
            # Assign variables from config file
            #
            self.srcdir   = config.get('Master', 'srcdir');
            self.builddir = config.get('Master', 'builddir');
            self.promodir = config.get('Master', 'promodir');
            self.port     = config.get('Master', 'port');

    def commandset(self):

        """
        Display help for all commands
        """

        #
        # Use an array for the return trip
        #
        ret = []

        #
        # Standard message
        #
        ret.append("bb commands:\n")

        #
        # Iterate through sorted supported commands
        #
        for cmd in sorted(self.cmdlist):

            ret.append(self.commands[cmd]['obj'].help())

        #
        # Append help to the return array
        #
        ret.append('\nuse "bb help [command]" for command specific help')

        #
        # Return the array
        #
        return ret

    def shutdown(self):

        SimpleXMLRPCServer.server_close(self.server)

    #
    # Command broker used for testing commands withput the use of RPC
    #
    def broker(self, *command):

        """
        Broker all requests to their respective functions
        """

        #
        # There's only 2 special cases for commands sent
        #
        if command[0] == 'commands':

            #
            # Return list of commands
            #
            return self.commandset()

        if command[0] == 'help':

            help = command[1][0]

            #
            # Return usage message
            #
            return self.commands[help]['obj'].usage()
        
        if command[0] == 'shutdown':

            #
            # shutdown the service
            #
            self.shutdown();

        #
        # If there's no args alog with the command name
        #
        if len(command) == 1:

            #
            # if no args are sent
            #
            return self.commands[command[0]]['obj'].bbcall()

        #
        # If there were args sent with the command...
        #
        else:

            #
            # Grab the first array in the tuple
            #
            args = command[1:][0]

            #
            # Send args to bbcall converting the array to a tuple
            #
            return self.commands[command[0]]['obj'].bbcall(tuple(args)[0:])

    def serve_forever(self):

        while not self.finished: 

            server.handle_request()

    #
    # Start RPCXML service and listen for events
    #
    def __loadrpcxml(self):

        #
        # Create the RPC service
        #
        try:

            self.server = SimpleXMLRPCServer(("0.0.0.0", int(self.port)))
            self.socket = self.server.socket

        #
        # If an exception was caught, display it and exit
        #
        except Exception, e:

            print "unable to start service:", e
            sys.exit(1)

        #
        # Use array for sorting supported command set
        #
        self.cmdlist = []

        #
        # Startup message
        #
        print "registering xmlrpc commands"

        #
        # Register all commands with the rpc service
        #
        for cmd in self.commands:

            self.cmdlist.append(cmd)
            #self.server.register_function(self.broker, cmd)
            #self.server.register_function(self.commands[cmd]['obj'].bbcall, cmd)

        #
        # Register the 'commands' command
        #
        self.server.register_function(self.commandset, 'commands')
        self.server.register_function(self.broker, 'broker')
        self.server.register_function(self.shutdown, 'shutdown')

        if self.debug:

            self.server.register_introspection_functions()

    def get_server(self):

        return self.server

