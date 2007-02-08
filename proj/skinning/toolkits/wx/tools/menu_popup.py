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

from menu import *

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class PopupMenu(wx.Menu):
    def __init__(self, window, *args, **kw):
        wx.Menu.__init__(self, *args, **kw)
        self.window = window

    def popup(self, *args, **kw):
        return self.popupOn(self.window, *args, **kw)

    def popupOn(self, window, *args, **kw):
        return window.PopupMenu(self, *args, **kw)
        
    def popupEvt(self, evt):
        return self.popup(evt.GetPosition())

    def getEvtHandler(self):
        return self

class menu_popup(menu):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    defaultSettings = menu.defaultSettings.copy()
    defaultSettings.update({ 
        'ctx-push':'1',
        })

    defaultStyleSettings = menu.defaultStyleSettings.copy()
    defaultStyleSettings.update({
        })

    objParentTypes = wxPySkinElement.objParentTypes
    _ctxHostObjNames = ('popup',)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Definitions 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def createWidget(self, parentObj):
        kwWX = self.getStyleSettingsCollection(('style',), localized=('title',))
        obj = PopupMenu(parentObj, **kwWX)
        return obj

    def getEvtHostObject(self):
        return self.getObject()

    def getEvtObject(self):
        return self.getObject().window

    def getEvtHandler(self):
        return self.getObject().getEvtHandler()

    def installDefaultEvent(self, evtHandler, evtObject, evtCallback):
        wx.EVT_RIGHT_UP(self.getObject().window, evtCallback)

