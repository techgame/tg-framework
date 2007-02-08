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
        layout>layout {layout-cfg:'1,EXPAND'}
        frame>layout>panel {layout-cfg:'1,EXPAND'}
    </style>

    <frame title='My Frame' show='1'>
        <layout>
            <panel>
                <layout>
                    <spacer/>
                    <xrc-panel layout-cfg='1,ALIGN_RIGHT' name='MyPanel' ref='xrc.xml'/>
                    <spacer/>
                    <xrc-panel layout-cfg='1,ALIGN_CENTER' name='MyPanel' ref='xrc.xml'/>
                    <spacer/>
                    <xrc-panel layout-cfg='1,' name='TestPanel'>
                        <resource>
                            <!-- Notice that the class is NOT a standard wx class -->
                            <object class="wxPanel" name="TestPanel">
                                <size>200,100</size>
                                <object class="wxStaticText" name="label1">
                                    <label>This blue panel is a class derived from wx.Panel,\nand is loaded by a custom XmlResourceHandler.</label>
                                    <pos>10,10</pos>
                                </object>
                            </object>
                        </resource>
                    </xrc-panel>
                    <spacer/>
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

