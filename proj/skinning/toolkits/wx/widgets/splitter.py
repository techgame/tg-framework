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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class splitter(wxPyWidgetSkinElement):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    elementLocals = wxPyWidgetSkinElement.elementLocals.copy()
    elementLocals.update({
        'horizontal':wx.SPLIT_HORIZONTAL,
        'vertical':wx.SPLIT_VERTICAL,
        'horiz':wx.SPLIT_HORIZONTAL,
        'vert':wx.SPLIT_VERTICAL,
        })

    defaultSettings = wxPyWidgetSkinElement.defaultSettings.copy()
    defaultSettings.update({ 
        })

    defaultStyleSettings = wxPyWidgetSkinElement.defaultStyleSettings.copy()
    defaultStyleSettings.update({
        'style': 'SP_3D | CLIP_CHILDREN',
        'orient': 'SPLIT_VERTICAL',
        'sash-pos': '300',
        'sash-min': '100',
        })

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Definitions 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def createWidget(self, parentObj):
        kwWX = self.getStyleSettingsCollectionWX(('style', 'pos', 'size'))
        obj = wx.SplitterWindow(parentObj, **kwWX)
        obj.SetSplitMode(self.getStyleSettingEval('orient'))
        obj.SetMinimumPaneSize(self.getStyleSettingEval('sash-min'))
        obj.SetSashPosition(self.getStyleSettingEval('sash-pos'))
        return obj

    def finishWidget(self, obj, parentObj):
        children = obj.GetChildren()
        if len(children) >= 2:
            # split with the first two windows
            w0, w1 = children[:2]
            if obj.GetSplitMode() == wx.SPLIT_HORIZONTAL:
                obj.SplitHorizontally(w0, w1)
            else:
                obj.SplitVertically(w0, w1)
        elif children:
            w0, = children
            obj.Initialize(w0)

    def installDefaultEvent(self, evtHandler, evtObject, evtCallback):
        wx.EVT_SPLITTER_SASH_POS_CHANGED(evtHandler, evtObject.GetId(), evtCallback)

