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
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class WindowExpander(object):
    def __init__(self, window, horizontal=False, vertical=False):
        self.window = window
        self.horizontal = horizontal
        self.vertical = vertical

    def canAdjust(self):
        try:
            return not self.window.IsMaximized() and not self.window.IsIconized() and not self.window.IsFullScreen()
        except AttributeError:
            return True

    def adjustDimensions(self, item, prepend=False, *args, **kw):
        if self.canAdjust():
            width, height = item.GetSize()
            try: 
                minsize = item.GetMinSize()
                width = max(width, minsize[0])
                height = max(height , minsize[1])
            except AttributeError: 
                pass

            if prepend:
                self.adjustDimensionsEx(-width, -height, width, height, *args, **kw)
            else:
                self.adjustDimensionsEx(0, 0, width, height, *args, **kw)

    def adjustDimensionsEx(self, dx,dy,dw,dh, horizontal=False,vertical=False, sign=1):
        if self.canAdjust():
            x,y,w,h = self.window.GetRect()
            if vertical or self.vertical: dx = dw = 0
            if horizontal or self.horizontal: dy = dh = 0

            self.window.SetDimensions(x+sign*dx, y+sign*dy, w+sign*dw, h+sign*dh, wx.SIZE_ALLOW_MINUS_ONE)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ExpandableBoxSizer(wx.BoxSizer):
    def __init__(self, expandwindow, orientation, enabled=False):
        wx.BoxSizer.__init__(self, orientation)
        self.setExpandingEnabled(enabled)

        self.expander = WindowExpander(expandwindow, orientation==wx.HORIZONTAL, orientation== wx.VERTICAL)

    def getExpandingEnabled(self, value):
        return self.expandingEnabled
    def setExpandingEnabled(self, value):
        self.expandingEnabled = value

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def Add(self, item, sizerOption=0, sizerFlag=0, sizerBorder=0):
        if self.expandingEnabled:
            self.expander.adjustDimensions(item, False)
            sizerOption = 0 # sizer option should be 0 in when in expanding mode
        return wx.BoxSizer.Add(self, item, sizerOption, sizerFlag, sizerBorder, False)

    def Prepend(self, item, sizerOption=0, sizerFlag=0, sizerBorder=0):
        if self.expandingEnabled:
            self.expander.adjustDimensions(item, True)
            sizerOption = 0 # sizer option should be 0 in when in expanding mode
        return wx.BoxSizer.Prepend(self, item, sizerOption, sizerFlag, sizerBorder, True)

    def Remove(self, item, *args, **kw):
        if self.expandingEnabled:
            for child in self.GetChildren():
                if child.GetWindow() is item:
                    width, height = child.GetSize()
                    wasPrepended = child.GetUserData()
                    break

            result = wx.BoxSizer.Remove(self, item, *args, **kw)

            if wasPrepended:
                self.expander.adjustDimensionsEx(width, height, -width, -height)
            else:
                self.expander.adjustDimensionsEx(0, 0, -width, -height)

        else:
            result = wx.BoxSizer.Remove(self, item, *args, **kw)

        return result

