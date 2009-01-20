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

from dockingCommon import DockingModel, XMLSkin

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Constants / Variables / Etc. 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

xmlSkin = XMLSkin("""<?xml version='1.0'?>
<skin xmlns='TG.skinning.toolkits.wx' xmlns:skin='TG.skinning.common.skin'>
    <style>
        frame {frame-main:1; locking:1; size:'800,600'}
        frame-mini {locking:1; size:'300,200'}
        frame>layout {layout-cfg:'1,EXPAND'}
        layout>layout {layout-cfg:'1,EXPAND'}
        frame>layout>panel {layout-cfg:'1,EXPAND'}
        *.alignCenter {layout-cfg:'0,ALIGN_CENTER'}
    </style>

    <frame title='My Frame' show='1'>
        <layout>
            <dock-host ctxobj='dhTop' side='top' model='ctx.model' />
                <layout>
                    <dock-host ctxobj='dhLeft' side='left' model='ctx.model' />

                    <skin:reference fromctx='ctx.model.xmlModelSkin'/>

                    <dock-host ctxobj='dhRight' side='right' model='ctx.model' />
                </layout>
            <dock-host ctxobj='dhBottom' side='bottom' model='ctx.model' />
        </layout>
        obj.Center()
    </frame>
</skin>
""")
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    DockingModel.fromSkin(xmlSkin).skinModel()

