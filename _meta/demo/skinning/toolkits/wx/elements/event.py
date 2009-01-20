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

from TG.skinning.toolkits.wx import wxSkinModel, XMLSkin

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Constants / Variables / Etc. 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

xmlSkin = XMLSkin("""<?xml version='1.0'?>
<skin xmlns='TG.skinning.toolkits.wx'>
    <style>
        layout * {layout-cfg: '0, EXPAND|ALL,10'}
    </style>
    <frame class='main' title='My Frame' show='1'>
        <event type='EVT_MOVE'>
            ctx.output.SetValue('Moved to: %s' % (evt.GetPosition(),))
        </event>
        <panel>
            <layout>
                <label text='Please move this frame to get events!' />
                <text ctxobj='output' />

                <panel style='VSCROLL | HSCROLL' bgcolor='#DDF'>
                    <layout>
                        <label text='Scroll Position:' />
                        <text ctxobj='scrollPos' />
                    </layout>
                    <event type='EVT_SCROLLWIN'>
                        obj.SetScrollPos(evt.GetOrientation(), evt.GetPosition())
                        ctx.scrollPos.SetValue('position: %d orientation: %s ' % (evt.GetPosition(),
                                {wx.HORIZONTAL:'Horizontal', wx.VERTICAL:'Vertical'}[evt.GetOrientation()]))
                    </event>
                </panel>
            </layout>
        </panel>
    </frame>
</skin>
""")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    wxSkinModel.fromSkin(xmlSkin).skinModel()

