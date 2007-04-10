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

class application(wxPySkinElement):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    defaultSettings = wxPySkinElement.defaultSettings.copy()
    defaultSettings.update({ 
        'ctxobj': 'application',
        })

    defaultStyleSettings = wxPySkinElement.defaultStyleSettings.copy()
    defaultStyleSettings.update({
        'exitOnFrameDelete': 'False',
        'name': 'wxPySkin App',
        'vendor': 'a wxPySkin using Vendor',
        })

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Definitions 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def isWindowObj(self):
        return False
    def getLayoutObj(self):
        return None
    def registerWithCollector(self, *args, **kw):
        pass

    def xmlInitStarted(self, elemBuilder):
        kwWX = self.getStyleSettingsCollectionWX(['exitOnFrameDelete'], localized=['name', 'vendor'])
        kwWX.rename(AppName='name', Vendor='vendor')

        app = self.getOrCreateApplication()

        for aname,aval in kwWX.items():
            if aval is not None:
                setattr(app, aname, aval)

        self.setObject(app)

        rootctx = self.getContext().rootScope()
        rootctx.mainLoop = self.mainLoop
        rootctx.application = self.getObject()

        self.initialStandardOptions()
        return wxPySkinElement.xmlInitStarted(self, elemBuilder)

    def xmlInitFinalized(self, elemBuilder):
        wxPySkinElement.xmlInitFinalized(self, elemBuilder)
        self.finalStandardOptions()

    def mainLoop(self):
        return self.getObject().MainLoop()

    def getOrCreateApplication(self):
        app = wx.GetApp()
        if app is None:
            app = wx.PySimpleApp()
        return app

