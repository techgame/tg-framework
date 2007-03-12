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

from TG.skinning.toolkits.wx._baseElements import *
from TG.skinning.toolkits.wx.layouts.layout import LayoutMixin
from TG.guiTools.wx import sizerTools

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class groupbox(LayoutMixin, wxPyWidgetSkinElement):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    defaultSettings = wxPyWidgetSkinElement.defaultSettings.copy()
    defaultSettings.update({ 
        })

    defaultStyleSettings = wxPyWidgetSkinElement.defaultStyleSettings.copy()
    defaultStyleSettings.update({
        'style': '0',
        'label': 'GroupBox',
        'orient': 'vertical',
        })

    orientationDefault = defaultStyleSettings['orient']
    orientationAliases = {
        'vert': 'vertical',
        'horiz':'horizontal',
        wx.VERTICAL: 'vertical',
        wx.HORIZONTAL: 'horizontal',
        }
    orientationFactories = {
        'vertical': (lambda parentObj: wx.StaticBoxSizer(parentObj, wx.VERTICAL)),
        'horizontal': (lambda parentObj: wx.StaticBoxSizer(parentObj, wx.HORIZONTAL)),
        }
    orientationFactories[None] = orientationFactories[orientationDefault]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Definitions 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def createWidget(self, parentObj):
        kwWX = self.getStyleSettingsCollectionWX(('style', 'pos', 'size'), localized=('label',))
        groupbox = wx.StaticBox(parentObj, **kwWX)
        layoutHost = self.getOrientationFactory()(groupbox)
        sizerTools.adjustLayoutContainerSizes(groupbox, layoutHost)
        self.initialStandardWindowOptions(groupbox)
        self.finalStandardWindowOptions(groupbox)
        self.groupbox = groupbox
        return layoutHost

    def finishWidget(self, layoutHost, parentObj):
        #self.setObject(layoutHost.GetStaticBox()) ## can lead to strange use cases either way
        pass

    def installDefaultEvent(self, evtHandler, evtObject, evtCallback):
        wx.EVT_LEFT_UP(evtHandler, evtCallback)
        wx.EVT_RIGHT_UP(evtHandler, evtCallback)
        wx.EVT_MIDDLE_UP(evtHandler, evtCallback)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getOrientation(self):
        orientation = self.getStyleSetting('orient').lower()
        orientation = self.orientationAliases.get(orientation, orientation)
        return orientation

    def getOrientationFactory(self):
        orient = self.getOrientation()
        if orient in self.orientationFactories:
            return self.orientationFactories[orient]
        else: return self.orientationFactories[None]

