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

import wx

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Utilities
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def wxVersion(match=None):
    result = '%d.%d.%d.%d' % wx.VERSION[:4]
    if match: 
        return result.startswith(match)
    else: return result

if hasattr(wx, 'ObjectPtr') and issubclass(wx.Object, wx.ObjectPtr):
    # get the base classes
    def wxClasses(*args):
        result = []
        for arg in args:
            if issubclass(arg, wx.ObjectPtr):
                arg, = arg.__bases__
            result.append(arg)
        return tuple(result)

else:
    def wxClasses(*args):
        return args

