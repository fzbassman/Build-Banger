#!/usr/bin/env python

from lib.bbServer import bbServer

bbserver = bbServer()

server = bbserver.get_server()

server.serve_forever()
