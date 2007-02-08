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
from TG.skinning.toolkits.wx import wxSkinModel, XMLSkin

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Constants / Variables / Etc. 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

xmlSkin = XMLSkin("""<?xml version='1.0'?>
<skin xmlns='TG.skinning.toolkits.wx'>
    <frame-mdi title='My MDI Parent' show='1'>
        <menubar>
            <menu index='0' text='File'>
                <item text='Close'>
                    <event>
                        ctx.frame.Close()
                    </event>
                </item>
            </menu>
        </menubar>
        obj.Center()
        <frame-mdi title='My MDI Child One' show='1'/>
        <frame-mdi title='My MDI Child Two' show='1'/>
        <frame-mdi title='My MDI Child Three' show='1'/>
        obj.Cascade()
    </frame-mdi>
</skin>
""")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    wxSkinModel.fromSkin(xmlSkin).skinModel()

