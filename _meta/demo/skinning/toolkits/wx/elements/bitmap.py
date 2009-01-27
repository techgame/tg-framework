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
        frame {frame-main:1; locking:1; size:'800,600'}
        frame>layout {layout-cfg:'1,EXPAND'}
        layout>layout {layout-cfg:'0,EXPAND'}
        frame>layout>panel {layout-cfg:'1,EXPAND'}
        label{layout-cfg:'0,ALIGN_RIGHT|ALIGN_CENTRE_VERTICAL|ALL,5'}
        * {bgcolor: white}
    </style>

    <frame title='My Frame' show='1'>
        <image ref='py.ico' for='icon'/>
        <layout fit='True'>
            <panel>
                <layout-grid-flex cols='2'>
                    <label text='Bitmap'/>
                    <bitmap>
                        <image ref='button-normal.jpg' />
                        <image ref='button-hover.jpg' for='hover'/>
                    </bitmap>
                    <label text='Bitmap Button'/>
                    <button-bitmap style='0'>
                        <image>
                            elem.openFrom('button-normal.jpg')
                        </image>
                        <!--image ref='button-normal.jpg' /-->
                        <image ref='button-disabled.jpg' for='disabled'/>
                        <image ref='button-down-hover.jpg' for='selected'/>
                        <image ref='button-hover.jpg' for='hover'/>
                    </button-bitmap>
                    <label text='Toggle Bitmap Button'/>
                    <button-bitmap-toggle style='0'>
                        <image ref='button-normal.jpg' />
                        <image ref='button-hover.jpg' for='hover'/>
                        <image ref='button-down.jpg' for='down'/>
                        <image ref='button-down-hover.jpg' for='hover-down'/>
                    </button-bitmap-toggle>
                </layout-grid-flex>
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


