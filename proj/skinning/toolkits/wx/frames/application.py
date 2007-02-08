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
        obj = self.createApplication()
        self.setObject(obj)

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

    def createApplication(self):
        return wx.PySimpleApp()

