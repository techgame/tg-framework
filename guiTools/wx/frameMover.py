#!/usr/bin/env python
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##~ Copyright (C) 2002-2004  TechGame Networks, LLC.
##~ 
##~ This library is free software; you can redistribute it and/or
##~ modify it under the terms of the BSD style License as found in the 
##~ LICENSE file included with this distribution.
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""EventHandlers that allow any window to act as a drag bar.

Primarily fills the need of having a "move handle" somewhere else than the
titlebar of the window."""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import weakref
import wx
from subjectEvtHandler import SubjectEvtHandler

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class FrameMover(object):
    AnyButton = -1
    LeftButton = 1
    MiddleButton = 2
    RightButton = 3
    DefaultButton = LeftButton
    Captured = False

    def __init__(self, host, frame, sizeFrame=(0,0), mouseButtonId=DefaultButton):
        self.strategy = MoverStrategy()
        self.strategy.SetMovementOptions(*sizeFrame)

        self.setFrame(frame)
        handler = SubjectEvtHandler.forEvtHandler(host)
        wx.EVT_MOUSE_EVENTS(handler, self.onMouseEvents)
        self.mouseButtonId = mouseButtonId

    def setFrame(self, frame):
        return self.strategy.setFrame(frame)

    def onMouseEvents(self, evt):
        evt.Skip()
        if evt.ButtonDown(self.mouseButtonId):
            self.onMouseDown(evt)
        elif evt.ButtonUp(self.mouseButtonId):
            self.onMouseUp(evt)
        elif evt.Dragging():
            self.onMouseMotion(evt)

    def onMouseDown(self, evt):
        if not self.Captured:
            self.Captured = True
            eo = evt.GetEventObject()
            self.offsetPos = eo.ClientToScreen(evt.GetPosition())
            self.strategy.onMouseDown(evt)
            eo.CaptureMouse()

    def onMouseUp(self, evt):
        if self.Captured:
            self.Captured = False

            del self.offsetPos
            self.strategy.onMouseUp(evt)

            evt.GetEventObject().ReleaseMouse()

    def onMouseMotion(self, evt):
        if self.Captured:
            self.strategy.onMouseMotion(evt)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MoverStrategy(object):
    def SetMovementOptions(self, horizontal=0, vertical=0):
        """
        horizontal:
           -1 size left side of frame
            0 move horizontally
            1 size right side of frame

        vertical:
           -1 size top side of frame
            0 move vertically
            1 size bottom side of frame
        """
        self.sizeFrame = horizontal, vertical

    def setFrame(self, frame):
        self.frame = weakref.proxy(frame)

    def onMouseDown(self, evt):
        eo = evt.GetEventObject()
        self.offsetPos = eo.ClientToScreen(evt.GetPosition())
        self.frameRect = tuple(self.frame.GetRect())
        clientSize = tuple(self.frame.GetClientSize())
        size = tuple(self.frame.GetSize())
        bestSize = tuple(self.frame.GetBestSize())
        self.minSize = (bestSize[0]+size[0]-clientSize[0], bestSize[1]+size[1]-clientSize[1])
        self.remainingSize = [x-y for x,y in zip(size, self.minSize)]

    def onMouseUp(self, evt):
        del self.offsetPos
        del self.frameRect
        del self.minSize

    def onMouseMotion(self, evt):
        deltaPos = evt.GetEventObject().ClientToScreen(evt.GetPosition())
        deltaRect = [0,0,0,0]
        for idx in (0,1):
            alpha = self.sizeFrame[idx]
            dp, dl = 0, 0
            if alpha < 0: # left/top sizing
                dp = alpha * (self.offsetPos[idx] - deltaPos[idx])
                dl = alpha * (deltaPos[idx] - self.offsetPos[idx])

                # but don't let us use up more space than we have!
                dp = min(dp, self.remainingSize[idx])
            elif alpha > 0: # bottom/right sizing
                dl = alpha * (deltaPos[idx] - self.offsetPos[idx])

            elif self.sizeFrame == (0,0): # move operation
                dp = deltaPos[idx] - self.offsetPos[idx]
            deltaRect[0 + idx], deltaRect[2 + idx] = dp, dl

        newRect = [x+y for x,y in zip(self.frameRect, deltaRect)]

        # Adjust for minsize
        newRect[2:4] = map(max, self.minSize, newRect[2:4])
        self.frame.SetDimensions(*newRect)

