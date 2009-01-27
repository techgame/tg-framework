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

import sys

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

_lineIsFromEndOfLastParameter = False

def getFrameFileAndLine(depth=0):
    frame = sys._getframe(1+depth)
    return (frame.f_code.co_filename, frame.f_lineno, _lineIsFromEndOfLastParameter)

def _testForPosition(*args):
    return getFrameFileAndLine(1)[1]

_simple, _multi = _testForPosition(), _testForPosition("""
                                            multiple
                                            line
                                            string
                                            constant
                                            """)
_lineIsFromEndOfLastParameter = (_multi > _simple)

