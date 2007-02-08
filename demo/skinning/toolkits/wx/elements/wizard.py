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
    <frame ctxobj='mainFrame'>
        <wizard title='My Wizard' show='1'>
            <image ref='wizard.jpg'/>
            <wizard-page>
                <layout>
                    <spacer/>
                    <label text='This is a skinned wizard!' tooltip='This is a tooltip'/>

                    <spacer/>
                    <radiobox choices='Skinning is fun, Yes it is' label='My Radio Box' layout-cfg='0,EXPAND|ALL,5'>
                        <event>print "You selected My RadioBox:", repr(evt.GetString())</event>
                    </radiobox>

                    <layout-spacer/>
                    <listbox select='-2' layout-cfg='1,EXPAND|ALL,5' tooltip='This is a tooltip'>
                        for i,n in enumerate(vars(wx).keys()[:100]):
                            obj.Append('%d: wx.%s' % (i, n))

                        <event>print "You selected My ComboBox:", repr(evt.GetString())</event>
                    </listbox>
                </layout>
            </wizard-page>
            <wizard-page>
                <layout>
                    <label text='This is the second page of the skinned wizard!'/>
                    <layout-spacer/>
                    <calendar layout-cfg='1,EXPAND|ALL,5'/>
                </layout>
            </wizard-page>

            <event>
                print "Wizard complete:", evt.GetPage()
            </event>
            <event type='EVT_WIZARD_PAGE_CHANGED'>
                print "Wizard page changed:", evt.GetDirection()
            </event>
            <event type='EVT_WIZARD_CANCEL'>
                print "Wizard page canceled:", evt.GetPage()
            </event>
        </wizard>
    </frame>
    ctx.mainFrame.Close()
</skin>
""")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    wxSkinModel.fromSkin(xmlSkin).skinModel()

