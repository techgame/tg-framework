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
    <frame ctxobj='frame' title='My Frame' show='1' locking='1'>
        <menubar>
            <menu text="My Frame's Menu">
                <menu-item text='Print Info' help='My first help string'>
                    <event>
                        print
                        print "First Item Evt:", evt.GetEventObject().GetTitle()
                        print 'elem name:', elem.__class__.__name__
                        print 'isinstance(obj, MenuItem):',
                        print isinstance(obj, MenuItem)
                        print 'ctx.frame is evt.GetEventObject():',
                        print ctx.frame is evt.GetEventObject()
                        print
                    </event>
                    <image-art art='ART_INFORMATION' size='16,16'/>
                </menu-item>

                <menu-break />

                <item text='Full Screen\\tF11' help='Shows My Frame on the entire screen'>
                    <event>
                        if ctx.frame.IsFullScreen():
                            ctx.frame.ShowFullScreen(False)
                        else:
                            ctx.frame.ShowFullScreen(True, FULLSCREEN_NOBORDER|FULLSCREEN_NOCAPTION)
                    </event>
                    <event type='EVT_UPDATE_UI'>
                        if ctx.frame.IsFullScreen():
                            obj.SetText('Restore from Full Screen\tF11')
                        else:
                            obj.SetText('Full Screen\tF11')
                    </event>
                </item>

                <item text='Maximize' help='Maximize My Frame'>
                    <event>
                        frame = ctx.frame
                        if frame.IsMaximized():
                            frame.Restore()
                        else:
                            frame.Maximize()
                    </event>
                    <event type='EVT_UPDATE_UI'>
                        if ctx.frame.IsMaximized():
                            obj.SetText('Restore')
                            obj.SetHelp('Maximize My Frame')
                        else:
                            obj.SetText('Maximize')
                            obj.SetHelp('Restores My Frame from Maximized State')
                    </event>
                </item>

                <break />

                <menu-item text='Close|Alt-X' help='Close My Frame'>
                    <event>
                        ctx.frame.Close()
                    </event>
                </menu-item>
            </menu>
        </menubar>
        <toolbar>
        </toolbar>

        <splitter>
            <panel bgcolor='#AAFFAA'>
            </panel>
            <panel bgcolor='#AAAAFF'>
            </panel>
        </splitter>

        <statusbar>
        </statusbar>
        obj.Center()
    </frame>
</skin>
""")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    wxSkinModel.fromSkin(xmlSkin).skinModel()

