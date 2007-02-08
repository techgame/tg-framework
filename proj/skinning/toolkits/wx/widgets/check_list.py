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

from TG.guiTools.wx.listColumnSizers import ListColumnWidthSizerMixin

from TG.skinning.engine.xmlSkinner import XMLFactory
from TG.skinning.toolkits.wx._baseElements import *

from TG.skinning.toolkits.wx.tools import image_list
from TG.skinning.toolkits.wx.tools import list_item
from TG.skinning.toolkits.wx.tools import list_column

from TG.guiTools.wx import checkListCtrl

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class check_list(image_list.ImageListHandlerMixin, wxPyWidgetSkinElement):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    elementGlobals = wxPyWidgetSkinElement.elementGlobals.copy()
    elementGlobals.update({
        'ListItem': checkListCtrl.ListItem,
        'Item': checkListCtrl.ListItem,

        'ListColumnItem': checkListCtrl.ListColumnItem,
        'ListColumn': checkListCtrl.ListColumnItem,
        'Column': checkListCtrl.ListColumnItem,
        })

    xmlFactories = XMLFactory.Collection({
        (namespace, 'column'): XMLFactory.Static(list_column.list_column),
        (namespace, 'item'): XMLFactory.Static(list_item.list_item),

        None: XMLFactory.InheritFromNext(),
        }).setName('toolbar')

    defaultSettings = wxPyWidgetSkinElement.defaultSettings.copy()
    defaultSettings.update({ 
        })

    defaultStyleSettings = wxPyWidgetSkinElement.defaultStyleSettings.copy()
    defaultStyleSettings.update({
        'style':    'LC_ICON',
        'columns':  '',
        'column-widths': '()',
        'choices':  '',
        })

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Definitions 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def xmlInitStarted(self, elemBuilder):
        result = wxPyWidgetSkinElement.xmlInitStarted(self, elemBuilder)
        elemBuilder.pushXMLFactories(self.xmlFactories)
        return result

    def xmlInitFinalized(self, elemBuilder):
        elemBuilder.popXMLFactories()
        return wxPyWidgetSkinElement.xmlInitFinalized(self, elemBuilder)

    def createWidget(self, parentObj):
        kwWX = self.getStyleSettingsCollectionWX(('style', 'pos', 'size'))
        obj = checkListCtrl.CheckListCtrl(parentObj, **kwWX)

        colWidths = self.getStyleSettingEval('column-widths')
        if colWidths:
            obj.setColumnWidths(colWidths)

        columns = self.getStyleSetting('columns').strip()
        if columns:
            columns = columns.split(',')
            for idx, column in enumerate(columns):
                column = self.localizedText(column.strip())
                obj.InsertColumn(idx, column)

        for idx, choice in enumerate(filter(None, self.getStyleSetting('choices').split(','))):
            choice = self.localizedText(choice.strip())
            if choice:
                obj.InsertStringItem(idx, choice)

        return obj

    def finishWidget(self, obj, parentObj):
        select = self.getStyleSettingEval('select', None)
        if select is not None:
            if select < 0:
                select = max(0, obj.GetItemCount()+select)
            select = min(select, obj.GetItemCount())
            obj.SetItemState(select, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)

    def installDefaultEvent(self, evtHandler, evtObject, evtCallback):
        wx.EVT_LIST_ITEM_SELECTED(evtHandler, evtObject.GetId(), evtCallback)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def addCollectedImageListChildElement(self, childElem, imageList, purposes):
        obj = self.getObject()
        for purpose in purposes:
            if purpose in ('', 'default', 'normal', 'large'): 
                obj.SetImageList(imageList, wx.IMAGE_LIST_NORMAL)
                obj.imageList = imageList
            elif purpose in ('all', ): 
                obj.SetImageList(imageList, wx.IMAGE_LIST_NORMAL)
                obj.imageList = imageList
                obj.SetImageList(imageList, wx.IMAGE_LIST_SMALL)
                obj.imageListState = imageList
                obj.SetImageList(imageList, wx.IMAGE_LIST_STATE)
                obj.imageListSmall = imageList
            elif purpose in ('small', ): 
                obj.SetImageList(imageList, wx.IMAGE_LIST_SMALL)
                obj.imageListSmall = imageList
            elif purpose in ('state', ): 
                obj.SetImageList(imageList, wx.IMAGE_LIST_STATE)
                obj.imageListState = imageList
            else: 
                raise ValueError('Unknown purpose for image list: \'%s\'' % purpose)
        return False

