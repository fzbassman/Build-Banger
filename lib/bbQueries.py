#!/usr/bin/env python

#
# Reusable queries for SQL used by bb
#

#
# Primary class
#
class bbQueries:

    def __init__(self, **kwds):

        self.queries = {

            1   : "insert into %s values (%s)",
            2   : "select * from %s where server='%s'",
            3   : "update buildservers set status='%s' where server='%s'",
            4   : "delete from buildservers where server='%s'",
            5   : "select * from configuration where server='%s' and "\
                  "title='%s'",
            6   : "select port from configuration where server='%s' and "\
                  "title='%s'",
            7   : "select sccs from configuration where server='%s' and "\
                  "title='%s'",
            8   : "select top,port,client from configuration where "\
                  "server='%s' and title='%s' and sccs='%s'"

        }

    def returnformatted(self, query, args):

        return self.queries[query] % args
