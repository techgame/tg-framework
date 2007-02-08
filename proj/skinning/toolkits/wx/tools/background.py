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

from TG.common.contextApply import ContextApply_p_s
from TG.skinning.toolkits.wx._baseElements import *
import image 

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class background(image.BitmapImageHandlerMixin, wxPyWidgetBaseSkinElement):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    defaultSettings = wxPyWidgetBaseSkinElement.defaultSettings.copy()
    defaultSettings.update({ 
        })

    defaultStyleSettings = wxPyWidgetBaseSkinElement.defaultStyleSettings.copy()
    defaultStyleSettings.update({
        'clear': 'True',
        'buffer': 'True',
        })

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Definitions 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def createWidget(self, parentObj):
        wx.EVT_ERASE_BACKGROUND(parentObj, self.onEraseBackground)
        self.backgrounds = []
        self.clear = self.getStyleSettingEval('clear')
        self.buffer = self.getStyleSettingEval('buffer')
        return None

    def finishWidget(self, obj, parentObj):
        pass

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def addCollectedBitmapChild(self, childElem, bitmap, purposes):
        for purpose in purposes:
            if purpose in ('','default','center', 'centered'):
                self.backgrounds.append(ContextApply_p_s(self.drawCentered, bitmap))
            elif purpose in ('tile','tiled'):
                self.backgrounds.append(ContextApply_p_s(self.drawTiledBackground, bitmap))
            elif purpose in ('screen',):
                self.backgrounds.append(ContextApply_p_s(self.drawScreenBackground, bitmap))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def onEraseBackground(self, evt):
        eo = evt.GetEventObject()
        dc = evt.GetDC() or wx.ClientDC(eo)
        if self.buffer:
            dc = wx.BufferedDC(dc, eo.GetSize())
        self.drawBackgrounds(eo, dc)

    def drawBackgrounds(self, eo, dc):
        if self.clear:
            bgBrush = wx.Brush(eo.GetBackgroundColour())
            dc.SetBackground(bgBrush)
            dc.Clear()
            dc.SetBackground(wx.NullBrush)

        for callable in self.backgrounds:
            callable(eo, dc)

    def drawCentered(self, eo, dc, bitmap):
        width, height = eo.GetClientSize()
        dw,dh = bitmap.GetWidth(), bitmap.GetHeight()
        x, y = (width-dw)/2, (height-dh)/2
        dc.DrawBitmap(bitmap, x,y, True)

    def drawTiledBackground(self, eo, dc, bitmap):
        width, height = eo.GetClientSize()
        dw,dh = bitmap.GetWidth(), bitmap.GetHeight()
        x = y = 0
        while y<height:
            while x<width:
                dc.DrawBitmap(bitmap, x,y, True)
                x += dw
            x = 0; y += dh

    def drawScreenBackground(self, eo, dc, bitmap):
        x0, y0 = eo.ScreenToClient((0,0))
        dw,dh = bitmap.GetWidth(), bitmap.GetHeight()
        x, y = x0+(1600-dw)/2,y0+(1200-dh)/2
        dc.DrawBitmap(bitmap, x,y, True)

