#!/usr/bin/env python

import socket

from lib.bbDatabase import bbDatabase

server = socket.gethostname()

db = bbDatabase()

newjob = (server, 'buildbanger', 'servername:9190', 
         'zbuild_trunk_profile', '/usr/src/bb/example', 
         'retail', '10', 'wallys comment', 'perforce', 'http:/xxx', '1', 
         '1', '0', '/var/bb/builds/example', '1', '1', 
         'QA@whatever.com', 'QA', 'promote.sh', 'BB-%S', 'BB-re', 
         'http://jira/xxx')

db.sql_insert('configuration', newjob)
