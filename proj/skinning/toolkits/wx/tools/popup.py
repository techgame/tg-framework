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

from TG.skinning.toolkits.wx._baseElements import *
from TG.guiTools.wx import lockingFrame
from TG.guiTools.wx.lockingFrame import LockSide
from TG.notifications.event import Event

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class PopupModel(wxPyCompoundModel):
    onShowing = Event.objProperty()
    onHiding = Event.objProperty()

    def lockToSelf(self, control, LockSideIndicies=(LockSide.bottom,LockSide.innerLeft), LockSizeIndicies=()):
        return lockingFrame.lockWindowsTogether(self.frame, control, LockSideIndicies, LockSizeIndicies)

    def lockTo(self, control, LockSideIndicies=(LockSide.bottom,LockSide.innerLeft), LockSizeIndicies=()):
        return lockingFrame.lockWindowsTogether(control, self.frame, LockSideIndicies, LockSizeIndicies)

    def lockToDesktop(self, LockSideIndicies=(LockSide.innerTop,LockSide.innerLeft), LockSizeIndicies=()):
        return lockingFrame.lockToDesktop(self.frame, LockSideIndicies, LockSizeIndicies)
        
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def GetPosition(self, *args, **kw):
        return self.frame.GetPosition(*args, **kw)
    def SetPosition(self, *args, **kw):
        return self.frame.SetPosition(*args, **kw)
    def GetSize(self, *args, **kw):
        return self.frame.GetSize(*args, **kw)
    def SetSize(self, *args, **kw):
        return self.frame.SetSize(*args, **kw)
    def GetRect(self, *args, **kw):
        return self.frame.GetRect(*args, **kw)
    def SetRect(self, *args, **kw):
        return self.frame.SetRect(*args, **kw)

    def Show(self, show=True):
        if self.frame.IsShown():
            if not show: 
                self.onHiding()
            self.frame.Show(show)
        elif show: 
            self.frame.Show(show)
            self.frame.Raise()
            self.onShowing()

    def Hide(self):
        self.Show(False)

    def onActivate(self, evt):
        if not evt.GetActive() and self.frame.IsShown():
            self.Hide()

    def onClose(self, evt):
        if evt.CanVeto():
            evt.Veto()
            self.Hide()
        else: evt.Skip()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class popup(wxPySkinUnifiedCompoundElement):
    CompoundModelFactory = PopupModel
    xmlSkin = XMLSkin("""<?xml version='1.0'?>
        <frame-popup ctxobj='host.frame' T-settings-='::settings'>
            <template xmlns='TG.skinning.common.skin' expand='::contents'/>

            <event type='EVT_ACTIVATE' run='ctx.host.onActivate(evt)' />
            <event type='EVT_CLOSE' run='ctx.host.onClose(evt)' />
        </frame-popup>
        """)

