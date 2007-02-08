#!/usr/bin/env python
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##~ Copyright (C) 2002-2004  TechGame Networks, LLC.
##~ 
##~ This library is free software; you can redistribute it and/or
##~ modify it under the terms of the BSD style License as found in the 
##~ LICENSE file included with this distribution.
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os
from TG.common import path

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def countPyFiles(countItems=('*.py',), fromPath=os.curdir, ):
    def codeFilter(line):
        line = line.strip()
        return not line.startswith('#')
    return count(countItems, fromPath, codeFilter)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def count(countItems=(), fromPath=os.curdir, filterfn=lambda x:True):
    result = dict([(key, []) for key in countItems])
    local = path.path(fromPath)
    for item in countItems:
        for match in local.walk(item):
            totalcount = 0
            linecount = 0
            for line in file(match, 'r'):
                if filterfn(line):
                    linecount += 1
                totalcount += 1
            result[item].append((linecount, totalcount))
    return result

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    for key, lcl in countPyFiles().iteritems():
        files,lines,total = len(lcl), sum([c[0] for c in lcl]), sum([c[1] for c in lcl])
        print 'For', key, 'there are:'
        print '    %-6d files,' % (files, )
        print '    %-6d lines of content,' % (lines, )
        print '    %-6d total lines,' % (total, )
        print '    %-6d lines of content per file,' % (lines/(files or 1), )
        print '    %-6d total lines per file,' % (total/(files or 1), )
        print '    %-6.1f comment and whitespace %%,' % (100.0*total/lines - 100.0,)

