#!/usr/bin/env python
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from TG.skinning.toolkits import wx
import aSkinKit
import aWidgetKit

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Constants / Variables / Etc. 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

xmlSkin = wx.XMLSkin("""<?xml version='1.0'?>
<skin xmlns='TG.skinning.toolkits.wx'
    xmlns:wk='aWidgetKit Extension for TG.skinning'
    xmlns:ask='TG.skinning:aSkinKit Extension' >

    <ask:frame title='A Skin Kit Frame' show='1'>
        <button label='A regular wx.Button' />

        <spacer/>

        <wk:widget />

        <spacer/>
    </ask:frame>
</skin>
""")

class ExtendedSkinModel(wx.SkinModel):
    xmlSkin = xmlSkin
    xmlSkinnerInstalls = [wx, aSkinKit, aWidgetKit]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    ExtendedSkinModel().skinModel()


