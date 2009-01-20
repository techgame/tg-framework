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
from button import button

if wxVersion() < '2.5':
    import wx.help as help
else:
    import wx as help

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class button_contexthelp(button):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    elementGlobals = button.elementGlobals.copy()
    elementGlobals.update(vars(help))

    defaultSettings = button.defaultSettings.copy()
    defaultSettings.update({ 
        'wxid':     'ID_CONTEXT_HELP',
        })

    defaultStyleSettings = button.defaultStyleSettings.copy()
    defaultStyleSettings.update({
        'style':    'BU_AUTODRAW',
        'provider': 'SimpleHelpProvider()',
        })

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Definitions 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def createWidget(self, parentObj):
        kwWX = self.getStyleSettingsCollectionWX(('style', 'pos', 'size'))
        obj = help.ContextHelpButton(parentObj, **kwWX)

        if help.HelpProvider_Get() is None:
            provider = self.getStyleSettingEval('provider')
            help.HelpProvider_Set(provider)
        
        return obj

    def installDefaultEvent(self, evtHandler, evtObject, evtCallback):
        wx.EVT_BUTTON(evtHandler, evtObject.GetId(), evtCallback)
