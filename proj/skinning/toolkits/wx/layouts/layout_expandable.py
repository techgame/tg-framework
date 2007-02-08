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

from TG.guiTools.wx.expandableSizers import ExpandableBoxSizer
from layout import *

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class layout_expandable(layout):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    defaultSettings = layout.defaultSettings.copy()
    defaultSettings.update({ 
        })

    defaultStyleSettings = layout.defaultStyleSettings.copy()
    defaultStyleSettings.update({
        })

    orientationDefault = layout.orientationDefault
    orientationFactories = {
        'vertical': (lambda parentObj, frame: ExpandableBoxSizer(frame, wx.VERTICAL)),
        'horizontal': (lambda parentObj, frame: ExpandableBoxSizer(frame, wx.HORIZONTAL)),
        }
    orientationFactories[None] = orientationFactories[orientationDefault]
    orientationFactories['opposite'] = orientationFactories[orientationDefault]
    orientationFactories['same'] = orientationFactories[orientationDefault]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Definitions 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def createWidget(self, parentObj):
        expandableSizerFactory = self.getOrientationFactory()
        obj = expandableSizerFactory(parentObj, self.getParentFrame())
        return obj

    def finishWidget(self, obj, parentObj):
        layout.finishWidget(self, obj, parentObj)
        obj.setExpandingEnabled(True)

