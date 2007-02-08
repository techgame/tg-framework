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

from TG.guiTools.wx.hoverEvents import ToggleBitmapButtonWithHover
from button_bitmap import *

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class button_bitmap_toggle(button_bitmap):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    defaultSettings = button_bitmap.defaultSettings.copy()
    defaultSettings.update({ 
        })

    defaultStyleSettings = button_bitmap.defaultStyleSettings.copy()
    defaultStyleSettings.update({
        'value': 'False',
        'hover': 'False',
        })

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Definitions 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def createWidget(self, parentObj):
        kwWX = self.getStyleSettingsCollectionWX(('style', 'pos', 'size'))
        kwWX['bitmap'] = self.emptyBitmap
        obj = ToggleBitmapButtonWithHover(parentObj, **kwWX)
        obj.SetValue(self.getStyleSettingEval('value'))
        obj.enableHover = self.getStyleSettingEval('hover')
        return obj

    def finishWidget(self, obj, parentObj):
        if obj.enableHover:
            obj.setupHover()

    def installDefaultEvent(self, evtHandler, evtObject, evtCallback):
        wx.EVT_BUTTON(evtHandler, evtObject.GetId(), evtCallback)

    def addCollectedBitmapChild(self, childElem, bitmap, purposes):
        obj = self.getObject()
        for purpose in purposes[:]:
            if purpose in ('up', 'up-normal', 'normal-up'): 
                obj.SetBitmapUp(bitmap) 
            elif purpose in ('up-hover', 'hover-up'): 
                obj.SetBitmapUpHover(bitmap)
                obj.enableHover = True
            elif purpose in ('down', 'down-normal', 'normal-down'): 
                obj.SetBitmapDown(bitmap)
            elif purpose in ('down-hover', 'hover-down'): 
                obj.SetBitmapDownHover(bitmap)
                obj.enableHover = True
            elif purpose in ('none',): 
                pass
            else: 
                continue
            purposes.remove(purpose)
        return button_bitmap.addCollectedBitmapChild(self, childElem, bitmap, purposes)

