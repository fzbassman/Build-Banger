#!/usr/bin/env python

#
# Package to handle all database operations for bb
#

#
# Import packages
#
import socket
import sqlite3
import os.path
import os
from bbQueries import bbQueries

hostname = socket.gethostname()
queries  = bbQueries()
dir      = os.getcwd()

sqlite3.enable_callback_tracebacks(True)

class bbDatabase:

    def __init__(self) :

        """
        Initialize bb's database.  If the database doesn't exist, it will
        be created automatically, the schema will be loaded and the server will
        register it's-self for use as a bb server or slave depending on what
        values are found in bb,ini
        """

        #
        # Structure for all bb tables, use for creation and upgrade
        #
        self.bbstruct = {

            'actions' : {

                'create' : 'CREATE TABLE actions ('\
                           'server varchar(30) default NULL,'\
                           'title varchar(30) default NULL,'\
                           'stepname text,'\
                           'parent blob,'\
                           'script blob,'\
                           'source blob,'\
                           'target blob'\
                           ')'

            },

            'activetestimage' : {

                'create' : 'CREATE TABLE activetestimage ('\
                           'server varchar(30) default NULL,'\
                           'deployserver varchar(30) default NULL,'\
                           'imagename varchar(64) default NULL,'\
                           'title varchar(30) default NULL,'\
                           'buildserver varchar(30) default NULL,'\
                           'jobname varchar(30) default NULL,'\
                           'job varchar(30) default NULL,'\
                           'installimage varchar(30) default NULL,'\
                           'imagereference varchar(30) default NULL'\
                           ')'

            },

            'authtable' : {

                'create' : 'CREATE TABLE authtable ('\
                           'server varchar(30) default NULL,'\
                           'machine varchar(128) default NULL'\
                           ')'

            },

            'buildservers' : {

                'create' : 'CREATE TABLE buildservers ('\
                           'server varchar(30) default NULL,'\
                           'description blob,'\
                           'port int(6) default NULL,'\
                           'status int(1) default NULL,'\
                           'globalmail varchar(64) default NULL,'\
                           'jobstatus int(1) default NULL'\
                           ')'

            },

            'changes' : {

                'create' : 'CREATE TABLE changes ('\
                           'server varchar(30) default NULL,'\
                           'title varchar(30) default NULL,'\
                           'job varchar(25) default NULL,'\
                           'changes text'\
                           ')'

            },

            'comments' : {

                'create' : 'CREATE TABLE comments ('\
                           'server varchar(30) NOT NULL default "",'\
                           'title varchar(30) NOT NULL default "",'\
                           'job varchar(25) NOT NULL default "",'\
                           'comment blob,'\
                           'PRIMARY KEY (server, title, job)'\
                           ')'

            },

            'configuration' : {

                'create' : 'CREATE TABLE configuration ('\
                           'server varchar(30) NOT NULL default "",'\
                           'title varchar(30) NOT NULL default "",'\
                           'port text,'\
                           'client text,'\
                           'top varchar(255) default NULL,'\
                           'type varchar(255) default NULL,'\
                           'keeplevel int(4) default NULL,'\
                           'comment longtext,'\
                           'sccs varchar(16) default NULL,'\
                           'browserlink longtext,'\
                           'state int(2) default NULL,'\
                           'spam int(1) default NULL,'\
                           'buildsize bigint(64) default NULL,'\
                           'output text,'\
                           'poll int(1) default NULL,'\
                           'priority int(1) default NULL,'\
                           'groupmail blob default NULL,'\
                           'grouping varchar(64) default NULL,'\
                           'promotecmd text,'\
                           'bugid text,'\
                           'bugregexp text,'\
                           'bugurl text,'\
                           'PRIMARY KEY  (server,title)'\
                           ')'

            },

            'custom' : {

                'create' : 'CREATE TABLE custom ('\
                           'server varchar(30) default NULL,'\
                           'title varchar(30) default NULL,'\
                           'property varchar(64) default NULL,'\
                           'PRIMARY KEY (server,title,property)'\
                           ')'

            },

            'excludes' : {

                'create' : 'CREATE TABLE excludes ('\
                           'server varchar(30) default NULL,'\
                           'title varchar(30) default NULL,'\
                           'excludes blob'\
                           ')'

            },

            'groupings' : {

                'create' : 'CREATE TABLE groupings ('\
                           'server varchar(30) default NULL,'\
                           'gname varchar(64) default NULL,'\
                           'kind varchar(256) default NULL,'\
                           'PRIMARY KEY (server,gname)'\
                           ')'

            },

            'joblog' : {

                'create' : 'CREATE TABLE joblog ('\
                           'server varchar(30) default NULL,'\
                           'title varchar(30) default NULL,'\
                           'message varchar(255) default NULL,'\
                           'step int(2) default NULL'\
                           ')'

            },

            'jobs' : {

                'create' : 'CREATE TABLE jobs ('\
                           'server varchar(30) NOT NULL default "",'\
                           'title varchar(30) NOT NULL default "",'\
                           'job varchar(25) NOT NULL default "",'\
                           'start int(15) default NULL,'\
                           'end int(15) default NULL,'\
                           'status int(2) default NULL,'\
                           'info blob,'\
                           'sccs varchar(16) default NULL,'\
                           'browserlink blob,'\
                           'buildsize bigint(64) default NULL,'\
                           'port varchar(64) default NULL,'\
                           'removed int(1) default NULL,'\
                           'releaseformat char(16) NOT NULL default "",'\
                           'PRIMARY KEY (server,title,job)'\
                           ')'

                },

            'keep' : {

                'create' : 'CREATE TABLE keep ('\
                           'server varchar(30) default NULL,'\
                           'title varchar(30) default NULL,'\
                           'job varchar(30) default NULL,'\
                           'at varchar(60) default NULL,'\
                           'bywhom varchar(60) default NULL,'\
                           'comment text'\
                           ')'

            },

            'locktest' : {

                'create' : 'CREATE TABLE locktest ('\
                           'server varchar(30) default NULL,'\
                           'title varchar(30) default NULL,'\
                           'buildjob varchar(30) default NULL'\
                           ')'

            },

            'monitorservers' : {

                'create' : 'CREATE TABLE monitorservers ('\
                           'server varchar(30) default NULL,'\
                           'port int(6) default NULL,'\
                           'status int(1) default NULL'\
                           ')'

            },

            'pending' : {

                'create' : 'CREATE TABLE pending ('\
                           'server varchar(30) default NULL,'\
                           'title varchar(30) default NULL,'\
                           'changes blob'\
                           ')'

            },

            'polltest' : {

                'create' : 'CREATE TABLE polltest ('\
                           'server varchar(30) default NULL,'\
                           'title varchar(30) default NULL'\
                           ')'

            },

            'proctree' : {

                'create' : 'CREATE TABLE proctree ('\
                           'server varchar(30) default NULL,'\
                           'title varchar(30) default NULL,'\
                           'job varchar(25) default NULL,'\
                           'cmd blob,'\
                           'pid int(64) default NULL'\
                           ')'

            },

            'promotion' : {

                'create' : 'CREATE TABLE promotion ('\
                           'server varchar(30) default NULL,'\
                           'title varchar(30) default NULL,'\
                           'job varchar(25) default NULL,'\
                           'at varchar(26) default NULL,'\
                           'bywhom varchar(60) default NULL,'\
                           'comment blob,'\
                           'state text'\
                           ')'

            },

            'removed' : {

                'create' : 'CREATE TABLE removed ('\
                           'server varchar(30) default NULL,'\
                           'title varchar(30) default NULL,'\
                           'job varchar(25) default NULL,'\
                           'at varchar(26) default NULL,'\
                           'action varchar(16) default NULL,'\
                           'directory blob'\
                           ')'

            },

            'restore' : {

                'create' : 'CREATE TABLE restore ('\
                           'server varchar(30) default NULL,'\
                           'title varchar(30) default NULL,'\
                           'message varchar(255) default NULL,'\
                           'time int(15) default NULL,'\
                           'state int(2) default NULL'\
                           ')'

            },

            'results' : {

                'create' : 'CREATE TABLE results ('\
                           'server varchar(30) default NULL,'\
                           'deployserver varchar(30) default NULL,'\
                           'title varchar(30) default NULL,'\
                           'buildserver varchar(30) default NULL,'\
                           'jobname varchar(30) default NULL,'\
                           'job varchar(30) default NULL,'\
                           'start int(15) default NULL,'\
                           'end int(15) default NULL,'\
                           'teststatus int(1) default NULL'\
                           ')'

            },

            'run' : {

                'create' : 'CREATE TABLE run ('\
                           'server varchar(30) default NULL,'\
                           'deployserver varchar(30) default NULL,'\
                           'title varchar(30) default NULL,'\
                           'buildserver varchar(30) default NULL,'\
                           'jobname varchar(30) default NULL,'\
                           'job varchar(30) default NULL,'\
                           'start int(15) default NULL,'\
                           'end int(15) default NULL,'\
                           'state int(1) default NULL,'\
                           'message blob,'\
                           'dependserver varchar(30) default NULL'\
                           ')'

            },

            'semaphores' : {

                'create' : 'CREATE TABLE semaphores ('\
                           'server varchar(30) default NULL,'\
                           'title varchar(30) default NULL,'\
                           'message varchar(255) default NULL,'\
                           'time int(15) default NULL,'\
                           'state int(2) default NULL'\
                           ')'

            },

            'serverids' : {

                'create' : 'CREATE TABLE serverids ('\
                           'server varchar(30) default NULL,'\
                           'type varchar(30) default NULL,'\
                           'pid varchar(30) default NULL'\
                           ')'

            },

            'stage' : {

                'create' : 'CREATE TABLE stage ('\
                           'server varchar(30) default NULL,'\
                           'deployserver varchar(30) default NULL,'\
                           'imagename varchar(64) default NULL,'\
                           'bootscript varchar(64) default NULL,'\
                           'title varchar(30) default NULL,'\
                           'buildserver varchar(30) default NULL,'\
                           'jobname varchar(30) default NULL,'\
                           'job varchar(30) default NULL,'\
                           'state int(1) default NULL,'\
                           'installimage varchar(30) default NULL,'\
                           'attempt int(1) default NULL,'\
                           'dependserver varchar(30) default NULL'\
                           ')'

            },

            'subscription' : {

                'create' : 'CREATE TABLE subscription ('\
                           'server varchar(30) default NULL,'\
                           'title varchar(30) default NULL,'\
                           'address varchar(64) default NULL'\
                           ')'

            },

            'testconfiguration' : {

                'create' : 'CREATE TABLE testconfiguration ('\
                           'server varchar(30) default NULL,'\
                           'title varchar(30) default NULL,'\
                           'type int(1) default NULL,'\
                           'imagename varchar(64) default NULL,'\
                           'bootscript varchar(64) default NULL,'\
                           'comment blob,'\
                           'state int(1) default NULL,'\
                           'nextjob varchar(30) default NULL,'\
                           'spam int(1) default NULL,'\
                           'buildjob varchar(30) default NULL,'\
                           'deployto varchar(30) default NULL,'\
                           'platform varchar(30) default NULL,'\
                           'imageserver varchar(30) default NULL,'\
                           'imagereference varchar(30) default NULL,'\
                           'attempts int(11) default NULL,'\
                           'dependserver varchar(30) default NULL,'\
                           'completed int(2) default NULL'\
                           ')'

            },

            'testserver' : {

                'create' : 'CREATE TABLE testserver ('\
                           'server varchar(30) default NULL,'\
                           'state int(1) default NULL'\
                           ')'

            },

            'teststate' : {

                'create' : 'CREATE TABLE teststate ('\
                           'title varchar(30) default NULL,'\
                           'buildserver varchar(30) default NULL,'\
                           'jobname varchar(30) default NULL,'\
                           'job varchar(30) default NULL,'\
                           'step varchar(30) default NULL,'\
                           'state int(1) default NULL,'\
                           'start int(15) default NULL,'\
                           'end int(15) default NULL,'\
                           'primary key (title, job)'\
                           ')'

            },

            'users' : {

                'create' : 'CREATE TABLE users ('\
                           'userid integer PRIMARY KEY AUTOINCREMENT,'\
                           'username varchar(30) NOT NULL default "",'\
                           'userpass varchar(32) NOT NULL default "",'\
                           'userrealm varchar(30) NOT NULL default "",'\
                           'realmid int(11) NOT NULL default "0",'\
                           'email varchar(64) default NULL'\
                           ')'

            },

        }

        if not os.path.exists('db'):

            os.mkdir('db')

        dbname = dir + "/db/bb.db"

        self.con = self.initdb(dbname)

    #
    # Initialize the DB if it doesn't exist
    #
    def initdb(self, name):

        """
        Figure out if the db dir exists, create if necessary and generate
        a new bb database
        """

        if not os.path.isfile(name):

            try:

                self.con = sqlite3.connect(name)
                #self.con.row_factory = sqlite3.Row
                self.cur = self.con.cursor()

                for db in self.bbstruct:

                    self.cur.execute(self.bbstruct[db]['create'])

            except e:

                print "Unable to 'create' database", e

        else:

            self.con = sqlite3.connect(name)
            #self.con.row_factory = sqlite3.Row

        return self.con

    #
    # Return the connection handle for the database
    #
    def getbbcon(self):

        """
        Return the database connection to whatever requests it
        """

        return self.con

    #
    # Insert record
    #
    def sql_insert(self, table, record):

        """
        Insert a record any of bb's tables.

        Args: tablename, tuple where tuple contains all values to be 
              submitted.  If the tuple doesn't have the args to match,
              a sqlite3 exception is thrown.
        """

        #
        # Create a cursor object
        #
        cur = self.con.cursor();

        #
        # Create a placeholder for the incoming record
        #
        picture = ",".join([str('?') for x in record])

        #
        # Format the query
        #
        query = queries.returnformatted(1, (table, picture))

        #
        # Execute this
        #
        try:

            cur.execute(query, record)
            self.con.commit()

        except sqlite3.Error, e:

            print "An error accured:", e.args[0]

    #
    # SQL Query 
    #
    def sql_query(self, query):

        """
        Query or update record(s) in the  bb database.  No records
        are returned if the query contains 'delete from'
        """

        rows = []

        #
        # convert the query to lower case for str.find
        #
        verify = query.lower()

        #
        # Don't allow 'delete from' to be used in sql_query
        #
        if verify.find('delete from') > -1:

            print "can't use delete from sql_query"
            return rows

        #
        # Create a cursor object
        #
        cur = self.con.cursor();

        #
        # Execute this
        #
        try:

            cur.execute(query)
            rows = cur.fetchall()

        except sqlite3.Error, e:

            print "An error accured:", e.args[0]

        return rows

    #
    # SQL Remove 
    #
    def sql_delete(self, query):

        """
        Delete record(s) from the bb database.  Cannot be used to query,
        or update records in bb
        """

        retval = False

        #
        # convert the query to lower case for str.find
        #
        verify = query.lower()

        #
        # Don't allow 'delete from' to be used in sql_query
        #
        if verify.find('delete from') == -1:

            print "no delete from statement found"
            return False

        #
        # Create a cursor object
        #
        cur = self.con.cursor();

        #
        # Execute this
        #
        try:

            cur.execute(query)
            rows = cur.fetchall()
            retval = True

        except sqlite3.Error, e:

            print "An error accured:", e.args[0]

        return retval

def bbtest():

    db.bbDatabase()

if __name__ == "main":

    bbtest()


