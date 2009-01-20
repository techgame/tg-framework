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

import time
import weakref
import os
import sets

import wx

from TG.skinning import resolvers
from TG.skinning.cssSkinModel import CSSSkinModel as _CSSSkinModelBase
from TG.skinning.engine import XMLFactory, XMLSkinner, XMLSkin
from TG.skinning.common import skin as CommonSkin

from TG.guiTools.wx import wxVersion

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Constants / Variables / Etc. 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

namespace = XMLFactory.xmlnsFromName(__name__)
namespaceSynonyms = {}
moduleCategories = (
    '',
    'widgets',
    'layouts',
    'events',
    'frames',
    'docking',
    'tools',
    'external',
    )
wxCSSMediumSet = ['toolkit-wx', 'toolkit-wx-'+wxVersion()]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def createXMLFactory(namespace=namespace):
    return XMLFactory.HierarchyNodeImport(__name__, moduleCategories)

def install(builder, namespace=namespace):
    builder.installSkins(CommonSkin)

    builder.xmlFactories.addFactory(namespace, createXMLFactory(namespace))
    builder.xmlnsSynonyms.update(namespaceSynonyms)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def _getOrCreateApplication():
    return wx.GetApp() or wx.PySimpleApp()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ wxSkinModel base
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class wxSkinModel(_CSSSkinModelBase):
    xmlSkinnerInstalls = [install]

    cssMediumSet = _CSSSkinModelBase.cssMediumSet.copy()
    cssMediumSet.update(wxCSSMediumSet)

    runSkin = True
    timeit = True

    def skinModel(self, **ctxvars):
        run = ctxvars.pop('run', self.runSkin)
        result = _CSSSkinModelBase.skinModel(self, **ctxvars)
        if run:
            ctx = result.ctx
            ctx.mainLoopReturn = self.runMainLoop(ctx)
        return result

    def run(self):
        app = wx.GetApp()
        return app.MainLoop()

    def runMainLoop(self, ctx):
        mainLoop = getattr(ctx, 'mainLoop', None)
        if mainLoop is None:
            mainLoop = ctx.application.MainLoop
        return mainLoop()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _getSkinModelContext(self, skinner, **ctxvars):
        ctxvars = _CSSSkinModelBase._getSkinModelContext(self, skinner, **ctxvars)
       
        # wxApp related attributes
        application = ctxvars.pop('application', None)
        if application is None:
            application = _getOrCreateApplication()
        if application is not None:
            ctxvars['application'] = application

        if 'gettext' not in ctxvars:
            ctxvars['gettext'] = self.getLocalizationEngine()
        return ctxvars

    def getLocalizationEngine(self):
        import gettext
        return gettext.gettext

SkinModel = wxSkinModel

