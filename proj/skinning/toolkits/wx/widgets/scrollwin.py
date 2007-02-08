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
from TG.guiTools.wx import sizerTools

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class scrollwin(wxPyWidgetSkinElement):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    defaultSettings = wxPyWidgetSkinElement.defaultSettings.copy()
    defaultSettings.update({ 
        })

    defaultStyleSettings = wxPyWidgetSkinElement.defaultStyleSettings.copy()
    defaultStyleSettings.update({
        'style':    'TAB_TRAVERSAL | HSCROLL | VSCROLL',
        'layout-cfg': '1, EXPAND',

        'rate': '20,20',
        #'size-virtual': '4000,4000',
        'size-hints': '0,0',
        })

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Definitions 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def createWidget(self, parentObj):
        kwWX = self.getStyleSettingsCollectionWX(('style', 'pos', 'size'))
        obj = wx.ScrolledWindow(parentObj, **kwWX)
        return obj

    def finishWidget(self, obj, parentObj):
        self.setupScrollRate(obj)

    def installDefaultEvent(self, evtHandler, evtObject, evtCallback):
        wx.EVT_SCROLLWIN(evtHandler, evtObject.GetId(), evtCallback)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def setupScrollRate(self, obj):
        rate = self.getStyleSettingEval('rate')
        w, h = obj.GetVirtualSize()
        if rate[0]:
            w += rate[0] - (w % rate[0])
        if rate[1]:
            h += rate[1] - (h % rate[1])
        obj.SetScrollRate(rate[0], rate[1])
        wx.CallAfter(obj.Scroll, 0, 0)

    def objSetSizer(self, obj, sizer, updateSizeHints=False, fitToSizer=False):
        # overridden to do virtual sizing
        obj.SetSizer(sizer)

        if updateSizeHints:
            sizerTools.adjustLayoutContainerSizes(obj, sizer, virtual=True)

        if fitToSizer:
            sizer.FitInside(obj)

