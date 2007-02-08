#!/usr/bin/env python
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~ Copyright (C) 2002-2005  TechGame Networks, LLC.              ##
##~                                                               ##
##~ This library is free software; you can redistribute it        ##
##~ and/or modify it under the terms of the BSD style License as  ##
##~ found in the LICENSE file included with this distribution.    ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from TG.skinning.toolkits.wxRender import RenderSkinModel, XMLSkin

xmlDodgeSkin = XMLSkin("""<?xml version='1.0'?>
<layer-group xmlns='TG.skinning.toolkits.wxRender'>
    <style xmlns='TG.skinning.common.skin'>
        layer-color { color: '#0000ff' }
        layer-color[for="hover"] { color: '#ffff00' }
    </style>

    <layer-group name='highlight'>
        <layer-image ref='reflection.png'  blend='blend'/>
        <layer-color color='#dddddd' />
    </layer-group>
    <layer-group name='ball'>

        <layer-group>
            <!--layer-image for='' ref='logo.png' blend='multiply'/>
            <layer-image for='hover, clicked' ref='logo.png' blend='dodge'/-->

            <layer-group blend='multiply'>
                <layer-text text='Some text for' pos='70,100' size='294, 294' color='black' />
                <layer-text text='Larry' pos='120,130' size='294, 294' color='white' />
            </layer-group>

            <layer-color for=''/>
            <layer-color for='hover' color='red'/>
            <layer-color for='clicked' color='green'/>
        </layer-group>
        <layer-group>
            <layer-image ref='base.png' blend='multiply'/>
            <layer-color />
        </layer-group>
    </layer-group>
    <layer-image name='shadow' ref='shadow.png'/>

    #obj._debugPrint()
    #obj._debugSave('comparisons/debug')
    obj.save('dodge-normal.png')
    obj.save('dodge-clicked.png', 'clicked')
    obj.save('dodge-hover.png', 'hover')
</layer-group>
""")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def render():
    RenderSkinModel.fromSkin(xmlDodgeSkin).skinModel()
    #RenderSkinModel.fromSkin(xmlMultiplySkin).skinModel()

if __name__=='__main__':
    render()

