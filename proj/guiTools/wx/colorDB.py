##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~ Copyright (C) 2002-2005  TechGame Networks, LLC.              ##
##~                                                               ##
##~ This library is free software; you can redistribute it        ##
##~ and/or modify it under the terms of the BSD style License as  ##
##~ found in the LICENSE file included with this distribution.    ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import wx
import sets

from TG.w3c.colors import colorToRGB_byte

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

_colourNames = None # sets.ImmutableSet
def colorFromDB(strColor):
    global _colourNames
    if _colourNames is None:
        from wx.lib import colourdb
        colourdb.updateColourDB()
        _colourNames = sets.ImmutableSet(colourdb.getColourList())

    strColor = strColor.upper()
    if strColor in _colourNames:
        return wx.NamedColor(strColor)
    return None

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def colorFromString(strColor, evalCB=eval):
    try: 
        color = colorToRGB_byte(strColor)
    except ValueError: 
        color = strColor
    else:
        if color is None:
            return color
        return wx.Color(*color)

    if strColor.startswith('SYS_COLOR'):
        color = wx.SystemSettings.GetColour(getattr(wx, strColor))
    elif color is None:
        color = colorFromDB(strColor)
        if color is None:
            color = wx.Color(*evalCB(strColor))
    return color

