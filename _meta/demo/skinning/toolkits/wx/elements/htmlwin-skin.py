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
<skin xmlns='TG.skinning.toolkits.wx' xmlns:skin='TG.skinning.common.skin'>
    <frame class='main' title='My Frame' show='1'>
        <layout>
            <panel help="This is my panel's help string">
                <layout>
                    <button-contexthelp/>

                    <htmlwin-skin layout-cfg='1,EXPAND' help='Html Widget with wx skin hooks enabled'>
                        <html xmlns='http://www.w3.org/1999/xhtml'>
                            <body>
                                <h1>My Heading</h1>
                                <p>Some text</p>

                                <h4>Part A &amp; B</h4>
                                <wxPySkin invoke='Part A'/>

                                <wxPySkin invoke='Part B'/>
                            </body>
                        </html>

                        <skin:section name='Part A'>
                            <panel size='200,200' help='A wx.Panel embedded in a wx.HtmlWindow'>
                                <layout>
                                    <groupbox label='Inside a "html-win" element' layout-cfg='1,EXPAND'>
                                        <label text='My Label'/>
                                        <line/>
                                        <button label='My Button'>
                                            <event>print "You pressed My Button"</event>
                                        </button>
                                    </groupbox>
                                </layout>
                            </panel>
                        </skin:section>
                        <skin:section name='Part B'>
                            <calendar help='A wx.CalendarCtrl embedded in a wx.HtmlWindow'>
                                <event>print "You selected My Calendar"</event>
                            </calendar>
                        </skin:section>
                    </htmlwin-skin>
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

