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

from TG.guiTools.wx import dockingTools
from TG.skinning.toolkits.wx._baseElements import *
from TG.skinning.toolkits.wx.layouts.layout import LayoutMixin

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class dock_host(wxPyWidgetBaseSkinElement):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    _ctxHostObjNames = ('dockhost', )

    defaultSettings = wxPyWidgetBaseSkinElement.defaultSettings.copy()
    defaultSettings.update({ 
        })

    defaultStyleSettings = wxPyWidgetBaseSkinElement.defaultStyleSettings.copy()
    defaultStyleSettings.update({
        'side': 'far',
        'hide-empty': 'False',
        'single': 'False',
        'model': 'None',
        })

    sideMap = {
        'true': True, 'false': False,
        'near': True, 'far': False,
        'left': True, 'right': False,
        'top': True, 'bottom': False,
        }

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Definitions 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def createWidget(self, parentObj):
        side = self.getStyleSetting('side').lower()
        prepend = self.sideMap.get(side, False)
        hideEmpty = self.getStyleSettingEval('hide-empty')

        layout = self.getLayoutBeforeParent(parentObj)
        obj = dockingTools.DockHost(parentObj, layout, prepend, hideEmpty)

        if self.getStyleSettingEval('single'):
            obj.setDockLimit(1)

        obj.setModel(self.getStyleSettingEval('model'))

        return obj

    def finishWidget(self, obj, parentObj):
        pass

    def getLayoutBeforeParent(self, parentObj):
        result = self.findXMLParentOrObjectOfType(LayoutMixin, self.objParentTypes)
        if result is not parentObj:
            return result.getObject()

