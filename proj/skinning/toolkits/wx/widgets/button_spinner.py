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

class button_spinner(wxPyWidgetSkinElement):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    defaultSettings = wxPyWidgetSkinElement.defaultSettings.copy()
    defaultSettings.update({ 
        })

    defaultStyleSettings = wxPyWidgetSkinElement.defaultStyleSettings.copy()
    defaultStyleSettings.update({
        'style':'SP_HORIZONTAL|SP_ARROW_KEYS',
        'value':'0',
        'min':'0',
        'max':'100',
        'bindTo': None,
        })

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Definitions 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def createWidget(self, parentObj):
        kwWX = self.getStyleSettingsCollectionWX(('style', 'pos', 'size'), localized=('label',))
        obj = wx.SpinButton(parentObj, **kwWX)

        min = self.getStyleSettingEval('min')
        max = self.getStyleSettingEval('max')
        obj.SetRange(min, max)

        bindTo = self.getStyleSettingEval('bindTo')
        if bindTo:
            bindTo.BindSpinButton(obj)

        value = self.getStyleSettingEval('value')
        obj.SetValue(value)

        return obj

    def finishWidget(self, obj, parentObj):
        pass

    def installDefaultEvent(self, evtHandler, evtObject, evtCallback):
        wx.EVT_SPIN(evtHandler, evtObject.GetId(), evtCallback)

