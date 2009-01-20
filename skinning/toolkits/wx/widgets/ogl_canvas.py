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

from scrollwin import *
from wx.lib.ogl import ShapeCanvas, OGLInitialize

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ogl_canvas(scrollwin):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    defaultSettings = scrollwin.defaultSettings.copy()
    defaultSettings.update({ 
        })

    defaultStyleSettings = scrollwin.defaultStyleSettings.copy()
    defaultStyleSettings.update({
        })

    def createWidget(self, parentObj):
        self.oglInitialize()

        kwWX = self.getStyleSettingsCollectionWX(('style', 'pos', 'size'))
        obj = ShapeCanvas(parentObj, **kwWX)
        return obj

    def finishWidget(self, obj, parentObj):
        result = scrollwin.finishWidget(self, obj, parentObj)
        self.setupScrollRate(obj)
        return result

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    _isOGLInitialized = False
    def oglInitialize(klass):
        if not klass._isOGLInitialized:
            OGLInitialize()
            klass._isOGLInitialized = True
    oglInitialize = classmethod(oglInitialize)

