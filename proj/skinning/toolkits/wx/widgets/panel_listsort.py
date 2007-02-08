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
import wx.lib.mixins.listctrl as listmix

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class PanelListSort(wx.Panel, listmix.ColumnSorterMixin):
    pass
    _itemMapData = None
    def getItemMapData(self):
        if self._itemMapData is None:
            pass #self.setItemMapData(None)
        return self._itemMapData
    def setItemMapData(self, itemMapData):
        self._itemMapData = itemMapData
    itemMapData = property(getItemMapData, setItemMapData)
    
    def GetListCtrl(self):
        return self.listCtrl

    _listCtrl = None
    def getListCtrl(self):
        return self._listCtrl
    def setListCtrl(self, listCtrl):
        self._listCtrl = listCtrl
    listCtrl = property(getListCtrl, setListCtrl)

    def initSorter(self, columns):
        listmix.ColumnSorterMixin.__init__(self, columns)

class panel_listsort(wxPyWidgetSkinElement):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    defaultSettings = wxPyWidgetSkinElement.defaultSettings.copy()
    defaultSettings.update({ 
        })

    defaultStyleSettings = wxPyWidgetSkinElement.defaultStyleSettings.copy()
    defaultStyleSettings.update({
        'style':    'TAB_TRAVERSAL|CLIP_CHILDREN',
        'layout-cfg': '1, EXPAND',
        })

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Definitions 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def createWidget(self, parentObj):
        kwWX = self.getStyleSettingsCollectionWX(('style', 'pos', 'size'))
        obj = PanelListSort(parentObj, **kwWX)
        return obj

    def finishWidget(self, obj, parentObj):
        pass


