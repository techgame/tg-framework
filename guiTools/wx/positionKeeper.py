#!/usr/bin/env python
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##~ Copyright (C) 2002-2004  TechGame Networks, LLC.
##~ 
##~ This library is free software; you can redistribute it and/or
##~ modify it under the terms of the BSD style License as found in the 
##~ LICENSE file included with this distribution.
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class PositionKeeper(object):
    def __init__(self, frame=None):
        if frame:
            self.SaveFrame(frame)

    def SaveFrame(self, frame):
        self.Dimensions = tuple(frame.GetRect())
        self.Shown = frame.IsShown() and 1 or 0
        self.Iconized = frame.IsIconized() and 1 or 0
        self.Maximized = frame.IsMaximized() and 1 or 0

    def RestoreFrame(self, frame):
        frame.SetDimensions(*self.Dimensions)
        frame.Iconize(self.Iconized)
        if not self.Iconized: frame.Maximize(self.Maximized)
        frame.Show(self.Shown)

