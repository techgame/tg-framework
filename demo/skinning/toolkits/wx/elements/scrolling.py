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
        frame {
            frame-main: True; 
            locking: True; 
            show: True;
        }

        frame>layout {layout-cfg:'1,EXPAND'}
        layout>layout {layout-cfg:'1,EXPAND|ALL,5'}
        frame>layout>panel {layout-cfg:'1,EXPAND'}

        #mylayout {orient:'horiz'}
        #mylayout>* {layout-cfg:'1,EXPAND|ALL,5'}

        image-list>image-art {size:inherit}
    </style>

    <frame title='Scrolled Windows in a Layout' pos='600,100'>
        <layout>
            <panel>
                <layout id='mylayout'>
                    <panel-scrolled page-name='Scrolled Panel Page'>
                        <layout hints='virtual'>
                            <reference xmlns='TG.skinning.common.skin' ref='largeLayout.skin'/>
                        </layout>
                    </panel-scrolled>

                    <scrollwin page-name='Scolled Page'>
                        <layout hints='virtual'>
                            <reference xmlns='TG.skinning.common.skin' ref='largeLayout.skin'/>
                        </layout>
                    </scrollwin>
                </layout>
            </panel>
        </layout>
    </frame>
    <frame title='Scrolled Windows in a Notebook' pos='100,100'>
        <layout>
            <panel>
                <layout id='mylayout'>
                    <notebook layout-minsize='400,300'>
                        <panel-scrolled page-name='Scrolled Panel Page'>
                            <layout hints='virtual'>
                                <reference xmlns='TG.skinning.common.skin' ref='largeLayout.skin'/>
                            </layout>
                        </panel-scrolled>

                        <scrollwin page-name='Scolled Page'>
                            <layout hints='virtual'>
                                <reference xmlns='TG.skinning.common.skin' ref='largeLayout.skin'/>
                            </layout>
                        </scrollwin>
                    </notebook>
                </layout>
            </panel>
        </layout>
    </frame>
</skin>
""")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    wxSkinModel.fromSkin(xmlSkin).skinModel()

