#!/usr/bin/env python

#
# Reusable errors used by bb
#

#
# Primary class
#
class bbErrors:

    def __init__(self, **kwds):

        self.errors = {

            1   : "no such job %s defined on %s"

        }

    def formatmsg(self, error, args):

        return self.errors[error] % args
