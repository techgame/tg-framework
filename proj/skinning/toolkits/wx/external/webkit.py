##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~ Copyright (C) 2002-2007  TechGame Networks, LLC.              ##
##~                                                               ##
##~ This library is free software; you can redistribute it        ##
##~ and/or modify it under the terms of the BSD style License as  ##
##~ found in the LICENSE file included with this distribution.    ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from TG.skinning.toolkits.wx._baseElements import *
import wx.webkit 
try:
    import wx.webview 
except ImportError:
    wx.webview = None

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class webkit(wxPyWidgetSkinElement):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    elementGlobals = wxPyWidgetSkinElement.elementGlobals.copy()
    elementGlobals.update(vars(wx.webkit))

    defaultSettings = wxPyWidgetSkinElement.defaultSettings.copy()
    defaultSettings.update({ 
        })

    defaultStyleSettings = wxPyWidgetSkinElement.defaultStyleSettings.copy()
    defaultStyleSettings.update({
        'layout-cfg': '1,EXPAND',
        'ref': 'http://www.python.org',

        })

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Definitions 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def createWidget(self, parentObj):
        kwWX = self.getStyleSettingsCollectionWX(['style', 'pos', 'size'], ['ref'])
        kwWX.rename(strURL='ref', winID='id')
        try:
            obj = wx.webkit.WebKitCtrl(parentObj, **kwWX)
        except NotImplementedError:
            if wx.webview is not None:
                return self.createWidgetFallback(parentObj)
            else: raise
        return obj

    _inFallback = False
    def createWidgetFallback(self, parentObj):
        kwWX = self.getStyleSettingsCollectionWX()
        obj = wx.webview.WebView(parentObj, **kwWX)
        self._inFallback = obj is not None
        return obj

    def finishWidget(self, obj, parentObj):
        ref = self.getStyleSetting('ref', None)
        if ref: obj.LoadURL(ref)

    def installDefaultEvent(self, evtHandler, evtObject, evtCallback):
        if self._inFallback:
            wx.webview.EVT_WEBVIEW_STATE_CHANGED(evtHandler, evtCallback)
        else:
            wx.webkit.EVT_WEBKIT_STATE_CHANGED(evtHandler, evtCallback)

