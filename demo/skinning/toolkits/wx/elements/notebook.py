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
                    <notebook layout-cfg='1,EXPAND'>
                        <image-list size='16,16'>
                            <image-art art='ART_INFORMATION' size='16,16' for='Me'/>
                            <image-art art='ART_QUESTION ' size='16,16'/>
                            <image-art art='ART_WARNING' size='16,16' for='you'/>
                        </image-list>

                        <panel page-name='File Browser' page-image='Me'>
                            <layout>
                                <reference xmlns='TG.skinning.common.skin' ref='fileExplorer.skin'/>
                            </layout>
                        </panel>
                        <page page-name='Pycrust' page-image='you'>
                            <layout>
                                <pycrust layout-cfg='1,EXPAND'/>
                            </layout>
                        </page>
                        <calendar page-name='Calendar' page-image='1'/>

                        <event>
                            print "You selected a page in My Notebook:", evt.GetString()
                            evt.Skip()
                        </event>
                    </notebook>
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

