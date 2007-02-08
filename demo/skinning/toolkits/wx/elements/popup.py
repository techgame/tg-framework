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
    <frame title='My Frame' show='True'>
        <layout>
            <panel>
                <layout>
                    <button label='Show My Popup'>
                        <event>
                            myPopup = ctx.myPopup
                            myPopup.lockTo(obj, 'bottom,cHoriz')
                            myPopup.Show()
                        </event>
                    </button>

                    <popup ctxobj='myPopup'>
                        <layout>
                            <button label='My Popup Button' >
                                <event>print "You pressed My Popup Button:", evt.GetEventObject()</event>
                            </button>
                            <slider ctxobj='myPopup.slider' value='40'>
                                <event>print "You used My Popup Slider:", repr(evt.GetInt())</event>
                            </slider>
                        </layout>

                        def onPopupShowing(self):
                            print "Showing!", self.slider.GetValue()
                        obj.onShowing = onPopupShowing
                        def onPopupHiding(self):
                            print "Hiding!", self.slider.GetValue()
                        obj.onHiding = onPopupHiding
                    </popup>
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

