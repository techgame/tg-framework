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

from TG.skinning.toolkits.wx._baseElements import XMLSkin, wxPySkinUnifiedCompoundElement, wxPyCompoundModel

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SkinKitFrameModel(wxPyCompoundModel):
    pass

class frame(wxPySkinUnifiedCompoundElement):
    CompoundModelFactory = SkinKitFrameModel
    xmlSkin = XMLSkin("""<?xml version='1.0'?>
        <frame T-settings-='::settings' size='800,600'
                xmlns='TG.skinning.toolkits.wx' 
                xmlns:ask='TG.skinning:aSkinKit Extension' >

            <ask:menubar/>

            <layout layout-cfg='1,EXPAND'>
                <panel layout-cfg='1,EXPAND'>
                    <layout layout-cfg='1,EXPAND' orient='horizontal'>
                        <template xmlns='TG.skinning.common.skin' expand='::contents'/>
                    </layout>
                </panel>
            </layout>

            <statusbar/>
        </frame>
        """)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    pass

