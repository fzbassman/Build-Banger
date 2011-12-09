#
# Command set exposed by bb
#

import os
import sys

class bbCommands:

    """
    Set of commands defining all functionality exposed via RPCXML
    for bb
    """

    def __init__(self, **kwds):

        self.commands = {}

    #
    # Load all python classes from cmdset directory
    #
    def loadcommands(self):

        #
        # Walk the cmdset tree looking for bb files
        #
        for root, dir, files in os.walk('./cmdset'):

            if len(dir) == 0:

                #
                # Iterate through files in the cmdset directory
                #
                for file in [f for f in files if f.endswith('.py')]:

                    #
                    # Make sure the filename starts with bb
                    #
                    if file.find('bb', 0) == 0 :

                        #
                        # Strip '.py' from the module
                        #
                        bbmodule = file.split('.')[0]

                        #
                        # The command is appended to the underscore
                        #
                        command     = bbmodule.split('_')[1]

                        #
                        # The module is cmdset.bb_module
                        #
                        module      = 'cmdset.' + bbmodule

                        #
                        # Import the module
                        #
                        imported    = __import__(module, globals(), locals(), 
                                                [bbmodule])

                        #
                        # Find the class in the module
                        #
                        moduleclass = getattr(imported, bbmodule)

                        #
                        # Create the object
                        #
                        object      = moduleclass()

                        #
                        # Display the command as it's loaded
                        #
                        print "loaded cmdset." + bbmodule + " as "\
                              + object.name + "..."

                        #
                        # Don't load objects with the same function defined
                        #
                        if not self.commands.has_key(object.name):

                            #
                            # Load the object into a command dictionary
                            #
                            self.commands[object.name] = { 'obj' : object }

    def admincommands(self):

        for entry in self.commands['admincmds']:

            module = 'lib.Commands.cab_' + entry
            cmd    = __import__(module)

            print cmd

    def usercommands(self):

        return self.commands['usercmds']
