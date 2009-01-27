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
from TG.guiTools.wx.sizerTools import HostLayoutLink

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class LayoutMixin(object):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Definitions 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getLayoutObjOf(self, elem):
        if isinstance(elem, wxPySkinElement):
            return elem.getLayoutObj()
        else: return None
    def getLayoutObj(self):
        return self.getObject()
    def getLayoutHost(self):
        return self.getObject()

    def isChildCollector(self):
        return True
    def addCollectedChild(self, childElem, childObj): 
        childLayoutObj = self.getLayoutObjOf(childElem)
        if childLayoutObj is not None:
            # Add to our layout object
            self.addLayoutChild(childElem, childLayoutObj)
            return False
        return self.__super.addCollectedChild(childElem, childObj)

    def addLayoutChild(self, childElem, childLayoutObj):
        host = self.getLayoutHost()
        self.addChildToLayout(host, childElem, childLayoutObj)
        self.updateChildLayoutMinsize(host, childElem, childLayoutObj)

    def addChildToLayout(self, host, childElem, childLayoutObj):
        args, kw = self.getChildLayoutArgs(host, childElem, childLayoutObj)
        hostSizerItem = host.Add(childLayoutObj, *args, **kw)
        HostLayoutLink.forLayoutObj(childLayoutObj, host, hostSizerItem)

    def getChildLayoutArgs(self, host, childElem, childLayoutObj):
        args = childElem.getStyleSettingEval('layout-cfg', ())
        if not isinstance(args, (tuple, list)):
            args = (args,)
        args = self.getChildLayoutBorderArgs(host, childElem, childLayoutObj, *args)
        return args, {}

    def getChildLayoutBorderArgs(self, host, childElem, childLayoutObj, proportion=0,flag=0,size=0, *args):
        borderFlag = childElem.getStyleSettingEval('layout-border', None)
        borderSize = None

        if isinstance(borderFlag, (list, tuple)):
            borderFlag, borderSize = borderFlag

        if borderFlag is not None:
            # update with border settings
            flag = (flag & ~wx.ALL) | (borderFlag & wx.ALL)

        if borderSize is None:
            size = childElem.getStyleSettingEval('layout-border-size', size)
        else: 
            size = borderSize

        return (proportion, flag, size) + args

    def updateChildLayoutMinsize(self, host, childElem, childLayoutObj):
        minsize = childElem.getLayoutMinSize()
        if minsize is not None:
            host.SetItemMinSize(childLayoutObj, *minsize)

LayoutMixin._LayoutMixin__super = super(LayoutMixin)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class LayoutBase(LayoutMixin, wxPyWidgetBaseSkinElement):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    elementLocals = wxPyWidgetBaseSkinElement.elementLocals.copy()
    elementLocals['virtual'] = 'virtual'
    elementLocals['VIRTUAL'] = elementLocals['virtual']
    elementLocals['inside'] = 'inside'
    elementLocals['INSIDE'] = elementLocals['inside']

    defaultSettings = wxPyWidgetBaseSkinElement.defaultSettings.copy()
    defaultSettings.update({ 
        })

    defaultStyleSettings = wxPyWidgetBaseSkinElement.defaultStyleSettings.copy()
    defaultStyleSettings.update({
        'layout-cfg': '1, EXPAND',
        'fit': 'False',
        'hints': 'True',
        })

    objParentTypes = wxClasses(LayoutMixin, wx.Sizer, wx.Window)

    def _getParentObj(self):
        return self.findXMLParentOrObjectOfType(self.objParentTypes)

    def finishWidget(self, obj, parentObj):
        self.updateLayoutMinSize()
        if isinstance(parentObj, self.windowTypes):
            self.installObjAsSizer(obj, parentObj)        

    def updateLayoutMinSize(self):
        minsize = self.getLayoutMinSize()
        if minsize is not None:
            self.getObject().SetMinSize(minsize)

    def installObjAsSizer(self, obj, parentObj):
        fit = self.getStyleSettingEval('fit')
        hints = self.getStyleSettingEval('hints')

        parent = self.findXMLParentOf(parentObj)
        parent.objSetSizer(parentObj, obj, hints, fit)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class layout(LayoutBase):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    defaultSettings = LayoutBase.defaultSettings.copy()
    defaultSettings.update({ 
        })

    defaultStyleSettings = LayoutBase.defaultStyleSettings.copy()
    defaultStyleSettings.update({
        'orient': 'opposite',
        })

    orientationDefault = 'vertical'
    orientationAliases = {
        'opp': 'opposite',
        'vert': 'vertical',
        'horiz':'horizontal',
        wx.VERTICAL: 'vertical',
        wx.HORIZONTAL: 'horizontal',
        }
    orientationOpposits = {
        None: orientationDefault,
        'vertical': 'horizontal',
        'horizontal': 'vertical',
        wx.VERTICAL: 'horizontal',
        wx.HORIZONTAL: 'vertical',
        }
    orientationFactories = {
        'vertical': (lambda parentObj: wx.BoxSizer(wx.VERTICAL)),
        'horizontal': (lambda parentObj: wx.BoxSizer(wx.HORIZONTAL)),
        }
    orientationFactories[None] = orientationFactories[orientationDefault]
    orientationFactories['opposite'] = orientationFactories[orientationDefault]
    orientationFactories['same'] = orientationFactories[orientationDefault]

    layoutOrientTypes = LayoutBase.objParentTypes

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Definitions 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def createWidget(self, parentObj):
        return self.getOrientationFactory()(parentObj)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getOrientation(self):
        orientation = self.getOrientationSpecified()
        orientation = self.orientationAliases.get(orientation, orientation)

        # Grab the window parent object, or the first layout derived parent
        layoutParent = self.getLayoutOrientationParents()
        if isinstance(layoutParent, layout): 
            # Figure out what type of sizer we should be creating
            if orientation == 'opposite':
                parentOrient = layoutParent.getOrientation()
                orientation = self.orientationOpposits.get(parentOrient, self.orientationDefault)
            elif orientation == 'same':
                orientation = layoutParent.getOrientation()
        if orientation in ('opposite', 'same'):
            orientation = self.orientationDefault

        return self.orientationAliases.get(orientation, orientation)

    def getOrientationSpecified(self):
        return self.getStyleSetting('orient').lower()

    def getLayoutOrientationParents(self):
        return self.findXMLParentOrObjectOfType(LayoutMixin, self.layoutOrientTypes)

    def getOrientationFactory(self):
        orient = self.getOrientation()
        if orient in self.orientationFactories:
            return self.orientationFactories[orient]
        else: return self.orientationFactories[None]

