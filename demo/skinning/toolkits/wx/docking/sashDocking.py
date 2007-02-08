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
        frame {frame-main:1; locking:1; size:'1024,768'}
        frame-mini {locking:1; size:'300,200'}
        frame>layout {layout-cfg:'1,EXPAND'}
        layout>layout {layout-cfg:'1,EXPAND'}
        frame>layout>panel {layout-cfg:'1,EXPAND'}
        *.alignCenter {layout-cfg:'0,ALIGN_CENTER'}
        sash {size: '200,200'; show:False; autosize: False;size-border:5;size-border-all:5}
        dock-host-sash {hide-empty:True}
    </style>

    <frame title='My Frame' show='1'>
        <layout-sash>
            <sash align='top'>
                <panel>
                    <layout>
                        <dock-host-sash ctxobj='dhTop' side='top'/>
                    </layout>
                </panel>
            </sash>

            <sash align='bottom'>
                <panel>
                    <layout>
                        <dock-host-sash ctxobj='dhBottom' side='bottom'/>
                    </layout>
                </panel>
            </sash>

            <sash align='left'>
                <panel>
                    <layout>
                        <dock-host-sash ctxobj='dhLeft' side='left'/> 
                    </layout>
                </panel>
            </sash>

            <sash align='right'>
                <panel>
                    <layout>
                        <dock-host-sash ctxobj='dhRight' side='right'/>
                    </layout>
                </panel>
            </sash>

            <skin:reference fromctx='ctx.model.xmlModelSkin'/>

        </layout-sash>

        obj.Center()
    </frame>
</skin>
""")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    DockingModel.fromSkin(xmlSkin).skinModel()

