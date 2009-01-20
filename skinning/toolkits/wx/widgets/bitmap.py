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

from TG.guiTools.wx.hoverEvents import StaticBitmapWithHover
from TG.skinning.toolkits.wx._baseElements import *
from TG.skinning.toolkits.wx.tools import image

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class bitmap(image.BitmapImageHandlerMixin, wxPyWidgetSkinElement):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    defaultSettings = wxPyWidgetSkinElement.defaultSettings.copy()
    defaultSettings.update({ 
        })

    defaultStyleSettings = wxPyWidgetSkinElement.defaultStyleSettings.copy()
    defaultStyleSettings.update({
        'hover': 'False',
        'size-img': 'inherit',
        })

    emptyBitmap = wx.EmptyBitmap(1,1)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Definitions 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def createWidget(self, parentObj):
        kwWX = self.getStyleSettingsCollectionWX(('style', 'pos', 'size'))
        kwWX['bitmap'] = self.emptyBitmap
        obj = StaticBitmapWithHover(parentObj, **kwWX)
        obj.enableHover = self.getStyleSettingEval('hover')
        return obj

    def finishWidget(self, obj, parentObj):
        if obj.enableHover:
            obj.setupHover()

    def installDefaultEvent(self, evtHandler, evtObject, evtCallback):
        wx.EVT_LEFT_UP(evtHandler, evtCallback)
        wx.EVT_RIGHT_UP(evtHandler, evtCallback)
        wx.EVT_MIDDLE_UP(evtHandler, evtCallback)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def addCollectedBitmapChild(self, childElem, bitmap, purposes):
        obj = self.getObject()
        for purpose in purposes:
            if purpose in ('', 'default', 'normal'): 
                obj.SetBitmapNormal(bitmap)
            elif purpose in ('hover',): 
                obj.SetBitmapHover(bitmap)
                obj.enableHover = True
            elif purpose in ('none',): 
                pass
            else: 
                raise ValueError('Unknown purpose for image: \'%s\'' % purpose)

        self._setSizeFromBitmap(obj, bitmap)
        return False

