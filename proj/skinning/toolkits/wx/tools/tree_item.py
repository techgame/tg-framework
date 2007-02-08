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

import wx.gizmos

from TG.skinning.toolkits.wx._baseElements import *
from TG.guiTools.wx import treeCtrl

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class tree_item(wxPyWidgetBaseSkinElement):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    defaultSettings = wxPyWidgetBaseSkinElement.defaultSettings.copy()
    defaultSettings.update({ 
        })

    defaultStyleSettings = wxPyWidgetBaseSkinElement.defaultStyleSettings.copy()
    defaultStyleSettings.update({
        'text': 'A tree item',
        'expanded': 'False',
        #'image': '-1',
        #'image-selected': '-1',
        })

    treeCtrlType = wxClasses(wx.TreeCtrl, wx.gizmos.TreeListCtrl)
    objParentTypes = treeCtrlType  + (treeCtrl.TreeItem,)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Definitions 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def createWidget(self, parentObj):
        obj = treeCtrl.TreeItem()
        self.initialTreeItemOptions(obj, parentObj)
        self.addToParent(obj, parentObj)
        return obj

    def finishWidget(self, obj, parentObj):
        self.finalTreeItemOptions(obj, parentObj)

    def addToParent(self, obj, parentObj):
        treeObj = self.getTreeParent(parentObj)
        if isinstance(parentObj, self.treeCtrlType):
            parentObj = None
        obj.addToTree(treeObj, parentObj)

    def initialTreeItemOptions(self, obj, parentObj):
        text = self.getStyleSettingLocalized('text')
        if text:
            obj.SetText(text)

        # image indexes
        imageIndex = self.getImageIndex('image', parentObj)
        if imageIndex is not None:
            obj.SetImage(imageIndex, wx.TreeItemIcon_Normal)

        imageIndex = self.getImageIndex('image-selected', parentObj)
        if imageIndex is not None:
            obj.SetImage(imageIndex, wx.TreeItemIcon_Selected)

        imageIndex = self.getImageIndex('image-expanded', parentObj)
        if imageIndex is not None:
            obj.SetImage(imageIndex, wx.TreeItemIcon_Expanded)

        imageIndex = self.getImageIndex('image-selected-expanded', parentObj)
        if imageIndex is not None:
            obj.SetImage(imageIndex, wx.TreeItemIcon_SelectedExpanded)

        # font and color
        font = self.getStyleFontSetting(None)
        if font:
            self.objSetFont(obj, font)
        fgColor = self.getStyleColorSetting('fgcolor', None)
        if fgColor is not None:
            obj.SetForegroundColour(fgColor)
        bgColor = self.getStyleColorSetting('bgcolor', None)
        if bgColor is not None:
            obj.SetBackgroundColour(bgColor)

    def finalTreeItemOptions(self, obj, parentObj):
        treeObj = self.getTreeParent(parentObj)
        expanded = self.getStyleSettingEval('expanded')
        if expanded:
            treeObj.Expand(obj.GetTreeId())

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def installDefaultEvent(self, evtHandler, evtObject, evtCallback):
        wx.EVT_TREE_ITEM_ACTIVATED(evtHandler, -1, evtCallback)

    def getEvtHostObject(self):
        return self.getObject()
    def getEvtObject(self):
        return None
    def getEvtHandler(self):
        treeCtrl = self.findXMLParentObjectOfType(self.treeCtrlType)
        obj = self.getObject()
        return treeCtrl.getItemEvtHandler(obj)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getImageIndex(self, settingName, parentObj):
        imageIndex = self.getStyleSetting(settingName, None)
        if not imageIndex: 
            return None
        elif imageIndex.isdigit(): 
            return int(imageIndex)
        else:
            return parentObj.imageList.getIndexForPurpose(imageIndex)

    def getTreeParent(self, parentObj):
        if isinstance(parentObj, self.treeCtrlType):
            return parentObj
        elif getattr(self._xmlBuildTemp, 'treeParent', None):
            return self._xmlBuildTemp.treeParent
        else:
            treeParent = self.findXMLParentObjectOfType(self.treeCtrlType)
            self._xmlBuildTemp.treeParent = treeParent
            return treeParent

