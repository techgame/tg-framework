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

from TG.skinning.toolkits.wx import wxSkinModel, XMLSkin

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Constants / Variables / Etc. 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

xmlSkin = XMLSkin("""<?xml version='1.0'?>
<skin xmlns='TG.skinning.toolkits.wx'>
    <frame class='main' title='My Frame' show='1'>
        def screenShot(clientOnly=True):
            '''Code derived from Section `4 Screen Capture`__

            This code is also available from TG.guiTools.wx.bitmapTools
            
            .. __: http://wiki.wxpython.org/index.cgi/WorkingWithImages 
            '''

            if clientOnly:
                ctxDC = wx.ClientDC(obj)
                w, h = obj.GetClientSize()
            else:
                ctxDC = wx.WindowDC(obj)
                w, h = obj.GetSize()

            bmp = wx.EmptyBitmap(w, h, ctxDC.GetDepth())
            memDC = wx.MemoryDCFromDC(ctxDC)
            memDC.SelectObject(bmp) 
            memDC.Blit(0,0,w,h, ctxDC, 0,0) 
            memDC.SelectObject(wx.NullBitmap) 
            return bmp

        obj.screenShot = screenShot

        <layout>
            <panel>
                <layout orient='horizontal'>
                    <reference ref='fileExplorer.skin'/>

                    <button label='Screen Shot'>
                        <event>
                            bmp = ctx.frame.screenShot(False)
                            bmp.SaveFile('screenshot-frame.bmp', wx.BITMAP_TYPE_BMP)

                            bmp = ctx.frame.screenShot(True)
                            bmp.SaveFile('screenshot-client.bmp', wx.BITMAP_TYPE_BMP)
                        </event>
                    </button>
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

