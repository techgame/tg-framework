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

from TG.skinning.engine.xmlSkinner import XMLFactory
from TG.skinning.toolkits.wx._baseElements import *

import warnings
warnings.warn("toolbar tool elements need to be implemented")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Tool Sub Elements
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ToolBase(wxPyWidgetSkinElement):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    defaultSettings = wxPyWidgetSkinElement.defaultSettings.copy()
    defaultSettings.update({ 
        })

    defaultStyleSettings = wxPyWidgetSkinElement.defaultStyleSettings.copy()
    defaultStyleSettings.update({
        })

    objParentTypes = (wx.ToolBar,)

class SimpleTool(ToolBase): pass
class RadioTool(ToolBase): pass
class CheckTool(ToolBase): pass
class ControlTool(ToolBase): pass
class SeperatorTool(ToolBase): pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class toolbar(wxPyWidgetSkinElement):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    xmlFactories = XMLFactory.Collection({
        (namespace, 'tool'): XMLFactory.Static(SimpleTool),
        (namespace, 'tool-radio'): XMLFactory.Static(RadioTool),
        (namespace, 'tool-check'): XMLFactory.Static(CheckTool),
        (namespace, 'tool-control'): XMLFactory.Static(ControlTool),
        (namespace, 'tool-break'): XMLFactory.Static(SeperatorTool),
        (namespace, 'break'): XMLFactory.Static(SeperatorTool),

        None: XMLFactory.InheritFromNext(),
        }).setName('toolbar')

    defaultSettings = wxPyWidgetSkinElement.defaultSettings.copy()
    defaultSettings.update({ 
        })

    defaultStyleSettings = wxPyWidgetSkinElement.defaultStyleSettings.copy()
    defaultStyleSettings.update({
        'style': 'TB_HORIZONTAL | NO_BORDER',
        })

    objParentTypes = wxPyWidgetSkinElement.frameTypes

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Definitions 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def xmlInitStarted(self, elemBuilder):
        result = wxPyWidgetSkinElement.xmlInitStarted(self, elemBuilder)
        elemBuilder.pushXMLFactories(self.xmlFactories)
        return result

    def xmlInitFinalized(self, elemBuilder):
        wxPyWidgetSkinElement.xmlInitFinalized(self, elemBuilder)
        elemBuilder.popXMLFactories()

    def createWidget(self, parentObj):
        kwWX = self.getStyleSettingsCollectionWX(('style',))
        obj = wx.ToolBar(parentObj, **kwWX)
        return obj

    def finishWidget(self, obj, parentObj):
        parentObj.SetToolBar(obj)

