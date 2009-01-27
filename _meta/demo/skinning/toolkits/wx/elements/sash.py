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
        frame>layout>panel {layout-cfg:'1,EXPAND'}
        layout.stretch{layout-cfg:'1,EXPAND'}
        layout.stretch>*{layout-cfg:'1,EXPAND'}
    </style>

    <frame title='My Frame' show='1'>
        <layout>
            <panel>
                <layout-sash ctxobj='sashLayout'>
                    <sash ctxobj='sash1' align='top' size-border-all='5' >
                        <panel>
                            <layout css-class='stretch' orient='horizontal'>
                                <layout>
                                    <button label='Hide'>
                                        <event>
                                            ctx.sash1.Hide()
                                            ctx.frame.Layout()
                                        </event>
                                    </button>
                                </layout>

                                <checklist select='-2' choices='item 1, item 2  , item 3'>
                                    <event>print "You selected My ListBox!:", evt.GetString()</event>
                                </checklist>

                                <listbox select='-2' choices='item 1, item 2  , item 3'>
                                    <event>print "You selected My ListBox!:", evt.GetString()</event>
                                </listbox>
                            </layout>
                        </panel>
                    </sash>


                    <layout>
                        <panel bgcolor='#88FF88'>
                            <layout>
                                <spacer layout-cfg='1,'/>
                                <layout layout-cfg='0,ALIGN_CENTER'>
                                    <button label='Layout!'>
                                        <event>
                                            ctx.sashLayout.Layout()
                                        </event>
                                    </button>
                                    <button label='Toggle Sash 1'>
                                        <event>
                                            ctx.sash1.Show(not ctx.sash1.IsShown())
                                            ctx.sashLayout.Layout()
                                        </event>
                                    </button>
                                    <button label='Toggle Sash 2'>
                                        <event>
                                            ctx.sash2.Show(not ctx.sash2.IsShown())
                                            ctx.sashLayout.Layout()
                                        </event>
                                    </button>
                                </layout>
                                <spacer layout-cfg='1,'/>
                            </layout>
                        </panel>
                    </layout>

                    <sash ctxobj='sash2' align='left' size-border='5' >
                        <panel>
                            <layout>
                                <button label='Hide' layout-cfg='0,EXPAND'>
                                    <event>
                                        ctx.sash2.Hide()
                                        ctx.sashLayout.Layout()
                                    </event>
                                </button>
                            </layout>
                        </panel>
                    </sash>
                </layout-sash>
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

