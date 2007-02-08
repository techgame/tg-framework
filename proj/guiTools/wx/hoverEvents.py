#!/usr/bin/env python
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##~ Copyright (C) 2002-2004  TechGame Networks, LLC.
##~ 
##~ This library is free software; you can redistribute it and/or
##~ modify it under the terms of the BSD style License as found in the 
##~ LICENSE file included with this distribution.
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""Provides a simple interface for creating hover events.

Note: Currently only works with Windows.
"""
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import wx

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class HoverBaseMixin:
    hoverState = None
    hoverUpdateInterval = 100 # milisecond response time

    def setupHover(self):
        self.setupHoverEx()
        self.refreshHover()

    def setupHoverEx(self):
        wx.EVT_LEAVE_WINDOW(self, self._setNormalBitmap)
        wx.EVT_ENTER_WINDOW(self, self._setHoverBitmap)

    def refreshHover(self):
        if self.hoverState:
            if self._checkStillHovering():
                self._changeToHoverBitmap()
        else:
            self._changeToNormalBitmap()

    def setHoverState(self, state):
        if state != self.hoverState:
            self.hoverState = state
            self.refreshHover()

    def _setNormalBitmap(self, evt):
        self.setHoverState(False)
        evt.Skip()
    def _setHoverBitmap(self, evt):
        self.setHoverState(True)
        evt.Skip()

    def _checkStillHovering(self):
        if self and self.hoverState:
            mousePos = wx.GetMousePosition()
            mousePos = self.ScreenToClient(mousePos)
            stillHovering = self.GetClientRect().Inside(mousePos)

            self.setHoverState(stillHovering)
            if stillHovering:
                self._registerRefresh(self._checkStillHovering)
                return True
        return False

    _refreshTimer = None
    def _registerRefresh(self, cb, *args, **kw):
        if self._refreshTimer is None:
            self._refreshTimer = wx.PyTimer(None)

        self._refreshTimer.notify = lambda: cb(*args, **kw)
        self._refreshTimer.Start(self.hoverUpdateInterval, wx.TIMER_ONE_SHOT)

    def _getBitmapDefaultFor(self, purpose):
        raise NotImplementedError, 'Subclass responsibility'
    def _changeToHoverBitmap(self):
        raise NotImplementedError, 'Subclass responsibility'
    def _changeToNormalBitmap(self):
        raise NotImplementedError, 'Subclass responsibility'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class HoverMixin(HoverBaseMixin):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    hoverBitmap = None
    normalBitmap = None

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def setupHoverEx(self):
        HoverBaseMixin.setupHoverEx(self)
        if self.GetBitmapHover() is None:
            self.SetBitmapHover(self._getBitmapDefaultFor('hover'))
        if self.GetBitmapNormal() is None:
            self.SetBitmapNormal(self._getBitmapDefaultFor('normal'))

    def GetBitmapNormal(self):
        return self.normalBitmap 
    def SetBitmapNormal(self, normal):
        self.normalBitmap = normal

    def GetBitmapHover(self):
        return self.hoverBitmap 
    def SetBitmapHover(self, hover):
        self.hoverBitmap = hover

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class StaticBitmapWithHover(HoverMixin, wx.StaticBitmap):
    def SetBitmapNormal(self, bitmap):
        HoverMixin.SetBitmapNormal(self, bitmap)
        self.SetBitmap(bitmap)
        
    def _getBitmapDefaultFor(self, purpose):
        return self.GetBitmap()

    def _changeToHoverBitmap(self):
        self.SetBitmap(self.GetBitmapHover())
        self.Refresh()

    def _changeToNormalBitmap(self):
        self.SetBitmap(self.GetBitmapNormal())
        self.Refresh()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class BitmapButtonWithHover(HoverMixin, wx.BitmapButton):
    def SetBitmapNormal(self, bitmap):
        HoverMixin.SetBitmapNormal(self, bitmap)
        self.SetBitmapLabel(bitmap)
        
    def _getBitmapDefaultFor(self, purpose):
        if purpose == 'hover':
            return self.GetBitmapFocus() or self.GetBitmapLabel()
        else:
            return self.GetBitmapLabel()

    def _changeToHoverBitmap(self):
        self.SetBitmapLabel(self.GetBitmapHover())
        self.Refresh()

    def _changeToNormalBitmap(self):
        self.SetBitmapLabel(self.GetBitmapNormal())
        self.Refresh()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ToggleBitmapButtonWithHover(BitmapButtonWithHover):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    normalUpBitmap = None
    hoverUpBitmap = None
    normalDownBitmap = None
    hoverDownBitmap = None
    value = False

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Definitions 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def setupHoverEx(self):
        BitmapButtonWithHover.setupHoverEx(self)
        wx.EVT_BUTTON(self, self.GetId(), self.onToggleButton)

    def onToggleButton(self, evt):
        self.SetValue(not self.GetValue())
        evt.Skip()

    def GetValue(self):
        return self.value
    def SetValue(self, value):
        self.value = value
        self.refreshHover()
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def GetBitmapUp(self):
        return self.normalUpBitmap or self.GetBitmapLabel()
    def SetBitmapUp(self, normalUpBitmap):
        self.normalUpBitmap = normalUpBitmap
    def GetBitmapUpHover(self):
        return self.hoverUpBitmap or self.GetBitmapDown()
    def SetBitmapUpHover(self, hoverUpBitmap):
        self.hoverUpBitmap = hoverUpBitmap

    def GetBitmapDown(self):
        return self.normalDownBitmap or self.GetBitmapSelected()
    def SetBitmapDown(self, normalDownBitmap):
        self.normalDownBitmap = normalDownBitmap
    def GetBitmapDownHover(self):
        return self.hoverDownBitmap or self.GetBitmapUp()
    def SetBitmapDownHover(self, hoverDownBitmap):
        self.hoverDownBitmap = hoverDownBitmap

    def GetBitmapHover(self):
        if self.GetValue():
            return self.GetBitmapDownHover()
        else:
            return self.GetBitmapUpHover()
    def SetBitmapHover(self, bitmap, value=value):
        if value is None: 
            value = self.GetValue()
        if value:
            self.SetBitmapDownHover(bitmap)
            self.SetBitmapUp(bitmap)
        else:
            self.SetBitmapUpHover(bitmap)
            self.SetBitmapDown(bitmap)

    def GetBitmapNormal(self):
        if self.GetValue():
            return self.GetBitmapDown()
        else:
            return self.GetBitmapUp()
    def SetBitmapNormal(self, bitmap, value=value):
        if value is None: 
            value = self.GetValue()
        if value:
            self.SetBitmapDown(bitmap)
            self.SetBitmapUpHover(bitmap)
        else:
            self.SetBitmapUp(bitmap)
            self.SetBitmapDownHover(bitmap)

