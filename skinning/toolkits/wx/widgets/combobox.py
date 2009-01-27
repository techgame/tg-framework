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

class combobox(wxPyWidgetSkinElement):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    defaultSettings = wxPyWidgetSkinElement.defaultSettings.copy()
    defaultSettings.update({ 
        })

    defaultStyleSettings = wxPyWidgetSkinElement.defaultStyleSettings.copy()
    defaultStyleSettings.update({
        'style':'0',
        'choices':'',
        'value':'',
        'select':'None',
        })

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Definitions 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def createWidget(self, parentObj):
        kwWX = self.getStyleSettingsCollectionWX(('style', 'pos', 'size'))
        obj = wx.ComboBox(parentObj, **kwWX)

        self.setObject(obj)
        self.setChoices(self.getStyleSetting('choices').split(','))
        return obj

    def finishWidget(self, obj, parentObj):
        value = self.getStyleSettingLocalized('value')
        if value:
            obj.SetValue(value)
        else:
            select = self.getStyleSettingEval('select', None)
            if select is not None:
                self.setSelection(select)

    def installDefaultEvent(self, evtHandler, evtObject, evtCallback):
        wx.EVT_COMBOBOX(evtHandler, evtObject.GetId(), evtCallback)
        wx.EVT_TEXT_ENTER(evtHandler, evtObject.GetId(), evtCallback)

    def setChoices(self, iterChoice):
        obj = self.getObject()
        for choice in iterChoice:
            choice = self.localizedText(choice.strip())
            if choice:
                obj.Append(choice)

    def setSelection(self, select):
        obj = self.getObject()
        if select < 0:
            select = max(0, obj.GetCount()+select)
        else:
            select = min(select, obj.GetCount() or None)
        if select is not None:
            obj.SetSelection(select)

