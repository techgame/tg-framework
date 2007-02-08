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

from frame import *
from TG.skinning.toolkits.wx.tools import image

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class frame_splash(wxPostCreateWidgetMixin, frame):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    defaultSettings = frame.defaultSettings.copy()
    defaultSettings.update({ 
        })

    defaultStyleSettings = frame.defaultStyleSettings.copy()
    defaultStyleSettings.update({
        'title': 'Splash Screen',
        'size': '300,300',
        'frame-main': 'False',
        'style': 'SIMPLE_BORDER|FRAME_NO_TASKBAR|STAY_ON_TOP',
        'style-splash': 'SPLASH_CENTRE_ON_SCREEN|SPLASH_TIMEOUT',
        'timeout': '1.0',
        })

    splashBitmap = wx.EmptyBitmap(1,1)

    def createFrame(self, winParent):
        splashStyle = self.getStyleSettingEval('style-splash')
        splashTimeout = int(self.getStyleSettingEval('timeout')*1000)
        kwWX = self.getStyleSettingsCollectionWX(('style', 'pos', 'size'))
        obj = wx.SplashScreen(self.splashBitmap, splashStyle, splashTimeout, winParent, **kwWX)
        return obj

    def addCollectedBitmapChild(self, childElem, bitmap, purposes):
        for purpose in purposes[:]:
            if purpose in ('', 'default', 'splash'): 
                self.setSplashBitmap(bitmap)
                purposes.remove(purpose)
        return frame.addCollectedBitmapChild(self, childElem, bitmap, purposes)

    def setSplashBitmap(self, bitmap):
        self.splashBitmap = bitmap 
        try:
            self._tmCreateWidget()
        finally:
            del self.splashBitmap
