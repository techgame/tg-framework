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

class SkinSashLayoutAlgorithm(wx.LayoutAlgorithm):
    _content = _host = None
    nonContentWindows = wxClasses(wx.SashWindow, wx.SashLayoutWindow)

    def __init__(self, hostWindow):
        wx.LayoutAlgorithm.__init__(self)
        self.setHostWindow(hostWindow)
        self.content = None

    def getHostWindow(self):
        return self._host
    def setHostWindow(self, host):
        self._host = host
        if self._host is not None:
            wx.EVT_SIZE(self._host, self.onSize)

    def findContentWindow(self):
        for child in self.getHostWindow().GetChildren():
            if not isinstance(child, self.nonContentWindows):
                return child
        else: 
            return None

    def getContentWindow(self):
        content = self._content
        if content is None:
            content = self.findContentWindow()
        return content
    def setContentWindow(self, content):
        self._content = content

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def Layout(self):
        self.LayoutWindow(self.getHostWindow(), self.getContentWindow())

    def onSize(self, evt):
        self.Layout()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class layout_sash(wxPyWidgetBaseSkinElement):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    defaultSettings = wxPyWidgetBaseSkinElement.defaultSettings.copy()
    defaultSettings.update({ 
        })

    defaultStyleSettings = wxPyWidgetBaseSkinElement.defaultStyleSettings.copy()
    defaultStyleSettings.update({
        'content': 'None',
        })

    sashWindows = wxClasses(wx.SashWindow, wx.SashLayoutWindow)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Definitions 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def createWidget(self, parentObj):
        obj = SkinSashLayoutAlgorithm(parentObj)
        return obj

    def finishWidget(self, obj, parentObj):
        content = self.getStyleSettingEval('content')
        if content is not None:
            obj.setContentWindow(content)

    def installDefaultEvent(self, evtHandler, evtObject, evtCallback):
        wx.EVT_CALCULATE_LAYOUT(evtHandler, evtObject.GetId(), evtCallback)

    def isChildCollector(self):
        return True
    def addCollectedChild(self, childElem, childObj): 
        if isinstance(childObj, self.sashWindows):
            setSashLayout = getattr(childObj, 'setSashLayout', None)
            if setSashLayout is not None:
                setSashLayout(self.getObject())
            return False
        return wxPyWidgetBaseSkinElement.addCollectedChild(self, childElem, childObj)
