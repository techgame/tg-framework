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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class dockable(wxPySkinSeparateCompoundElement):
    defaultSettings = wxPySkinCompoundElement.defaultSettings.copy()
    defaultSettings.update({
        })

    defaultStyleSettings = wxPySkinCompoundElement.defaultStyleSettings.copy()
    defaultStyleSettings.update({
        })

    xmlSkin = XMLSkin("""<?xml version='1.0'?>
        <frame-popup ctxobj='hostElem.frame' show='False' frame-main='False' T-settings-='::settings'>
            <layout>
                <dock-host>
                    <dock-container ctxobj='hostElem.obj'>
                        <template xmlns='TG.skinning.common.skin' expand='::contents'/>
                    </dock-container>
                </dock-host>
            </layout>

            <event type='EVT_CLOSE'>
                if evt.CanVeto():
                    obj.Hide()
                    evt.Veto()
                else: evt.Skip()
            </event>
        </frame-popup>
        """)

