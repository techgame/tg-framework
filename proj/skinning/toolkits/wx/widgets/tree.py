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
from TG.skinning.toolkits.wx.tools import image_list

from TG.guiTools.wx import treeCtrl

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class tree(image_list.ImageListHandlerMixin, wxPyWidgetSkinElement):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    elementGlobals = wxPyWidgetSkinElement.elementGlobals.copy()
    elementGlobals.update({
        'TreeItem': treeCtrl.TreeItem,
        'Item': treeCtrl.TreeItem,
        })

    defaultSettings = wxPyWidgetSkinElement.defaultSettings.copy()
    defaultSettings.update({ 
        })

    defaultStyleSettings = wxPyWidgetSkinElement.defaultStyleSettings.copy()
    defaultStyleSettings.update({
        'style':    'TR_DEFAULT_STYLE',
        'indent':   'None',
        })

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Definitions 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def createWidget(self, parentObj):
        kwWX = self.getStyleSettingsCollectionWX(('style', 'pos', 'size'))
        obj = treeCtrl.TreeCtrl(parentObj, **kwWX)
        return obj

    def finishWidget(self, obj, parentObj):
        indent = self.getStyleSettingEval('indent')
        if indent is not None:
            obj.SetIndent(indent)

    def installDefaultEvent(self, evtHandler, evtObject, evtCallback):
        wx.EVT_TREE_SEL_CHANGED(evtHandler, evtObject.GetId(), evtCallback)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def addCollectedImageListChildElement(self, childElem, imageList, purposes):
        # Note: SetButtonsImageList appears to not be implemented
        obj = self.getObject()
        for purpose in purposes:
            if purpose in ('', 'default', 'normal'): 
                obj.SetImageList(imageList)
            elif purpose in ('all',): 
                obj.SetImageList(imageList)
                obj.SetStateImageList(imageList)
                #obj.SetButtonsImageList(imageList)
            elif purpose in ('state',): 
                obj.SetStateImageList(imageList)
            #elif purpose in ('buttons',): 
            #    obj.SetButtonsImageList(imageList)
            else: 
                raise ValueError('Unknown purpose for image list: \'%s\'' % purpose)
        return False

