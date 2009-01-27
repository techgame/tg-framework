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

from TG.guiTools.wx import bookCtrl

from TG.skinning.toolkits.wx._baseElements import *
from TG.skinning.toolkits.wx.tools import image_list

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class notebook(image_list.ImageListHandlerMixin, wxPyWidgetSkinElement):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    defaultSettings = wxPyWidgetSkinElement.defaultSettings.copy()
    defaultSettings.update({ 
        })

    defaultStyleSettings = wxPyWidgetSkinElement.defaultStyleSettings.copy()
    defaultStyleSettings.update({
        'style': '0',
        })

    _layoutObj = None

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Definitions 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def createWidget(self, parentObj):
        kwWX = self.getStyleSettingsCollectionWX(('style', 'pos', 'size'))
        obj = bookCtrl.Notebook(parentObj, **kwWX)
        return obj

    def finishWidget(self, obj, parentObj):
        pass

    def installDefaultEvent(self, evtHandler, evtObject, evtCallback):
        wx.EVT_NOTEBOOK_PAGE_CHANGED(evtHandler, evtObject.GetId(), evtCallback)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def isChildCollector(self):
        return True
    def addCollectedChild(self, childElem, childObj): 
        if isinstance(childObj, self.windowTypes):
            return self.addCollectedPage(childElem, childObj)
        return self.__super.addCollectedChild(childElem, childObj)
            
    def addCollectedPage(self, childElem, childObj):
        obj = self.getObject()
        pageName = childElem.getStyleSettingLocalized('page-name')
        pageSelect = childElem.getStyleSettingEval('page-select', False)
        pageIdx = childElem.getStyleSettingEval('page-idx', None)
        pageImage = childElem.getStyleSetting('page-image', None)

        if not pageImage: 
            pageImage=-1
        elif pageImage.isdigit(): 
            pageImage = int(pageImage)
        else:
            pageImage = obj.imageList.getIndexForPurpose(pageImage)

        if pageIdx >= 0:
            obj.InsertPage(pageIdx, childObj, pageName, pageSelect, pageImage)
        else:
            obj.AddPage(childObj, pageName, pageSelect, pageImage)
            pageIdx = obj.GetPageCount() - 1

        childElem.setSetting('page-idx-value', pageIdx)
        return False

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def addCollectedImageListChildElement(self, childElem, imageList, purposes):
        obj = self.getObject()
        for purpose in purposes:
            if purpose in ('', 'default', 'normal'): 
                obj.imageList = imageList
                obj.SetImageList(imageList)
            else: 
                raise ValueError('Unknown purpose for image list: \'%s\'' % purpose)
        return False
notebook._notebook__super = super(notebook)

