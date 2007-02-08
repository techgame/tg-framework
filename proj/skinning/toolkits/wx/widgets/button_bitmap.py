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

from TG.guiTools.wx.hoverEvents import BitmapButtonWithHover
from TG.skinning.toolkits.wx._baseElements import *
from TG.skinning.toolkits.wx.tools import image
from button import button

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class button_bitmap(image.BitmapImageHandlerMixin, button):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    defaultSettings = button.defaultSettings.copy()
    defaultSettings.update({ 
        })

    defaultStyleSettings = button.defaultStyleSettings.copy()
    defaultStyleSettings.update({
        'default':  '0',
        'label': '',
        'style': '0',
        'hover': 'False',
        })

    emptyBitmap = wx.EmptyBitmap(1,1)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Definitions 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def createWidget(self, parentObj):
        kwWX = self.getStyleSettingsCollectionWX(('style', 'pos', 'size'))
        kwWX['bitmap'] = self.emptyBitmap
        obj = BitmapButtonWithHover(parentObj, **kwWX)
        obj.enableHover = self.getStyleSettingEval('hover')
        return obj

    def finishWidget(self, obj, parentObj):
        if obj.enableHover:
            obj.setupHover()
        return button.finishWidget(self, obj, parentObj)

    def installDefaultEvent(self, evtHandler, evtObject, evtCallback):
        wx.EVT_BUTTON(evtHandler, evtObject.GetId(), evtCallback)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def addCollectedBitmapChild(self, childElem, bitmap, purposes):
        obj = self.getObject()
        for purpose in purposes:
            if purpose in ('', 'default', 'normal', 'up'): 
                obj.SetBitmapNormal(bitmap)
            elif purpose in ('selected','down'): 
                obj.SetBitmapSelected(bitmap)
            elif purpose in ('focus',): 
                obj.SetBitmapFocus(bitmap)
            elif purpose in ('hover',): 
                obj.SetBitmapHover(bitmap)
                obj.enableHover = True
            elif purpose in ('disabled',): 
                obj.SetBitmapDisabled(bitmap)
            elif purpose in ('label',): 
                obj.SetBitmapSelected(bitmap)
            elif purpose in ('none',): 
                pass
            else: 
                raise ValueError('Unknown purpose for image: \'%s\'' % purpose)

        self._setSizeFromBitmap(obj, bitmap)
        return False

