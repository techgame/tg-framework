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
        frame {frame-main:1; locking:1; size:800,600}
        panel>layout>* {layout-cfg:1,EXPAND; layout-border:ALL,5}
        panel>layout>line {layout-cfg:0,EXPAND; layout-border:ALL,None; layout-border-size:10}
        panel>layout>label {layout-cfg:0,EXPAND; layout-border:LEFT,5}

        layout.bar {fit: True; layout-cfg:0,EXPAND; layout-border:ALL,2}
        layout.bar>label {layout-cfg:0,0; layout-border:ALL,2}
        layout.bar>spacer {layout-cfg:1,0; layout-border:ALL,2}
        layout.bar>button {layout-cfg:0,0; layout-border:ALL,2}

        layout-grid>* {layout-cfg:1,EXPAND; layout-border:ALL,2}
        layout-grid-flex>* {layout-cfg:1,EXPAND; layout-border:ALL,2}
        layout-table>* {layout-cfg:1,EXPAND; layout-border:ALL,2}
    </style>

    <frame title='My Frame' show='1'>
        <layout>
            <panel>
                <layout orient='vertical'>
                    <layout class='bar'>
                        <label text='Static Layout Grid:'/>
                        <spacer />
                        <button label='-'>
                            <event>obj.SetLabel("+-"[ctx.layoutGrid.layoutLink.ShowToggle()])</event>
                        </button>
                    </layout>
                    <layout-grid ctxobj='layoutGrid' cols='3' >
                        <button label='r0 c0' /> <button label='r0 c1' /> <button label='r0 c2' />
                        <button label='r1 c0' /> <button label='r1 c1' /> <button label='r1 c2' />
                        <button label='r2 c0' /> <button label='r2 c1' /> <button label='r2 c2' />
                    </layout-grid>

                    <line />

                    <layout class='bar'>
                        <label text='Flexible Layout Grid:'/>
                        <spacer />
                        <button label='-'>
                            <event>obj.SetLabel("+-"[ctx.layoutGridFlex.layoutLink.ShowToggle()])</event>
                        </button>
                    </layout>
                    <layout-grid-flex ctxobj='layoutGridFlex' cols='3' grow-cols='0,-1' direction='HORIZONTAL' mode='FLEX_GROWMODE_ALL'>
                        <button label='r0 c0' /> <button label='r0 c1' /> <button label='r0 c2' />
                        <button label='r1 c0' /> <button label='r1 c1' /> <button label='r1 c2' />
                        <button label='r2 c0' /> <button label='r2 c1' /> <button label='r2 c2' />
                    </layout-grid-flex>

                    <line />

                    <layout class='bar'>
                        <label text='Layout Table:'/>
                        <spacer />
                        <button label='-'>
                            <event>obj.SetLabel("+-"[ctx.layoutTable.layoutLink.ShowToggle()])</event>
                        </button>
                    </layout>
                    <layout-table ctxobj='layoutTable'>
                        <button label='r0c0:h1w2' layout-ex='pos=(0,0),size=(1,2)' /> <button label='r0c2' layout-ex='pos=(0,2)' />
                        <button label='r1c0:h2w1' layout-ex='pos=(1,0),size=(2,1)' /> <button label='r1c1:h2w2' layout-ex='pos=(1,1),size=(2,2)' />
                        <button label='r3c0:h1w3' layout-ex='pos=(3,0),size=(1,3)' /> 
                    </layout-table>
                </layout>
            </panel>
        </layout>
        obj.Center()
    </frame>

</skin>
""")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    wxSkinModel.fromSkin(xmlSkin).skinModel()


