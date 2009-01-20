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

import wx
from TG.guiTools.wx import wxVersion, wxClasses

from colorDB import colorFromString
from listColumnSizers import ListColumnWidthSizerMixin
from itemEvtReflection import ReflectedListEvents, ItemModelSupportMixin, ItemEventModelSupportMixin, ItemEvtHandler

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ListItemBase(wx.ListItem):
    GetForegroundColour = wx.ListItem.GetTextColour
    SetForegroundColour = wx.ListItem.SetTextColour

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def setValues(self, text=None, imageIdx=None, align=None, font=None, fgColor=None, bgColor=None, data=None, column=None):
        mask = 0

        if text is not None:
            self.SetText(text)
            mask|=wx.LIST_MASK_FORMAT

        if imageIdx is not None:
            self.SetImage(imageIdx)
            mask|=wx.LIST_MASK_IMAGE

        if align is not None:
            self.SetAlign(align)
            mask|=wx.LIST_MASK_FORMAT

        if font is not None:
            self.SetFont(font)
        if fgColor is not None:
            fgColor = colorFromString(fgColor)
            self.SetTextColour(fgColor)
        if bgColor is not None:
            fgColor = colorFromString(bgColor)
            self.SetBackgroundColour(bgColor)

        if data is not None:
            self.SetData(data)
            mask|=wx.LIST_MASK_DATA

        if column is not None:
            self.SetColumn(column)

        self.SetStateMask(mask)

    def addToList(self, listCtrl, index=None, column=None):
        if column is not None:
            self.SetColumn(column)
        listCtrl.addListItemEx(self, index, self.GetColumn())

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def fromFromList(klass, listCtrl, itemid):
        result = listCtrl.GetItem(itemid)
        result.__class__ = klass
        return result
    fromFromList = classmethod(fromFromList)

    def updateToList(self, listCtrl):
        listCtrl.SetItem(self)
        return self

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ListRowEventModel(ItemEvtHandler):
    def getItemEvtHandler(self, listCtrl):
        return self

    def addItem(self, listItem):
        pass

class ListItem(ListItemBase, ItemModelSupportMixin):
    ListRowModelFactory = ListRowEventModel

    def addToList(self, listCtrl, index=None, column=None):
        ListItemBase.addToList(self, listCtrl, index=index, column=column)
        self.installItemModel(listCtrl)

    def installItemModel(self, listCtrl):
        listCtrl.setItemPyData(self, self)
        rowModel = listCtrl.getRowPyData(self, None)
        if rowModel is None:
            rowModel = self.ListRowModelFactory()
            listCtrl.setRowPyData(self, rowModel)

        rowModel.addItem(self)

    def getItemEvtHandler(self, listCtrl):
        rowModel = listCtrl.getRowPyData(self)
        return rowModel.getItemEvtHandler(listCtrl)

class ListColumnItem(ListItemBase, ItemEventModelSupportMixin):
    proportion = 0
    def addToList(self, listCtrl, index=None, column=None):
        assert index in (0, None)
        if column is not None:
            self.SetColumn(column)
        else:
            column = self.GetColumn()

        listCtrl.addListColumn(self, column)
        listCtrl.setRelColumnWidth(column, self.getProportion())
        self.installItemModel(listCtrl)

    def getProportion(self): 
        return self.proportion 
    def setProportion(self, proportion): 
        self.proportion = proportion 

    def installItemModel(self, treeWin):
        treeWin.setColumnPyData(self, self)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ ListCtrl related
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ListCtrlBase(wx.ListCtrl):
    """Adds support for get/setItemPyData"""

    _pyData = {}
    ListItemClasses = wxClasses(wx.ListItem)

    def getItemModel(self, itemOrId):
        item = self.getItemPyData(itemOrId, None)
        if item:
            return item.getItemModel()
        else: return None
    def getItemEvtHandler(self, itemOrId):
        item = self.getItemPyData(itemOrId, None)
        if item:
            return item.getItemEvtHandler(self)
        else: return None

    def getColumnModel(self, itemOrId):
        columnItem = self.getColumnPyData(itemOrId, None)
        if columnItem:
            return columnItem.getItemModel()
        else: return None
    def getColumnItemEvtHandler(self, itemOrId):
        columnItem = self.getColumnPyData(itemOrId, None)
        if columnItem:
            return columnItem.getItemEvtHandler(self)
        else: return None

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ PyData accessors
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    #~ By Item (cell) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getItemAndPyDataKey(self, itemOrId, keyDefault=None):
        item = self.getItemFromId(itemOrId)
        return item, ('cell', item.GetId(), item.GetColumn())

    def getItemPyData(self, itemOrId, default=NotImplemented):
        item, key = self.getItemAndPyDataKey(itemOrId)
        return self.getPyDataByKey(key, default)
    def setItemPyData(self, itemOrId, pyData, keyDefault=None):
        item, key = self.getItemAndPyDataKey(itemOrId, keyDefault)
        self.setPyDataByKey(key, pyData)

    #~ By Row ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getRowModelAndPyDataKey(self, itemOrId, keyDefault=None):
        item = self.getItemFromId(itemOrId)
        return item, ('row', item.GetId())

    def getRowPyData(self, itemOrId, default=NotImplemented):
        item, key = self.getRowModelAndPyDataKey(itemOrId)
        return self.getPyDataByKey(key, default)
    def setRowPyData(self, itemOrId, pyData, keyDefault=None):
        item, key = self.getRowModelAndPyDataKey(itemOrId)
        self.setPyDataByKey(key, pyData)

    #~ By Column ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getColumnItemAndPyDataKey(self, itemOrId, keyDefault=None):
        item = self.getItemFromId(itemOrId)
        return item, ('column', item.GetColumn())

    def getColumnPyData(self, itemOrId, default=NotImplemented):
        item, key = self.getColumnItemAndPyDataKey(itemOrId)
        return self.getPyDataByKey(key, default)
    def setColumnPyData(self, itemOrId, pyData, keyDefault=None):
        item, key = self.getColumnItemAndPyDataKey(itemOrId)
        self.setPyDataByKey(key, pyData)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ PyData foundations
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def clearAllPyData(self):
        self._pyData.clear()

    def getPyDataByKey(self, dataKey, default=NotImplemented):
        if default is NotImplemented:
            return self._pyData[dataKey]
        else: 
            return self._pyData.get(dataKey, default)
    def setPyDataByKey(self, dataKey, pyData):
        if not self._pyData:
            # lazy initialization
            self._pyData = {}
        self._pyData[dataKey] = pyData

    def getItemFromId(self, itemOrId):
        if not isinstance(itemOrId, self.ListItemClasses):
            result = self.GetItem(itemOrId)
        else: 
            result = itemOrId
        return result or None

    def ClearAll(self):
        self.clearAllPyData()
        return wx.ListCtrl.ClearAll(self)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ListCtrlExtended(ListCtrlBase):
    ListItemFactory = ListItem

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def addListColumn(self, lc, column):
        if column < self.GetColumnCount():
            self.SetColumn(column, lc)
        else:
            self.InsertColumnInfo(column, lc)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def addItem(self, index=None, column=0, *args, **kw):
        li = self.ListItemFactory()
        li.setValues(*args, **kw)
        li.addToList(self, index, column)
        return li

    def addListItem(self, listitem, *args, **kw):
        try:
            return listitem.addToList(self, *args, **kw)
        except AttributeError:
            return self.addListItemEx(listitem, *args, **kw)

    def addListItemEx(self, li, index=None, column=0):
        count = self.GetItemCount()
        if index is None:
            if column > 0:
                index = count-1
            else: 
                index = count
        elif index < 0:
            index = max(count + index, 0)

        index = min(index, count)

        li.SetId(index)
        li.SetColumn(column)

        if index >= count:
            self.InsertItem(li)
        else:
            self.SetItem(li)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ListCtrl(ListCtrlExtended, ListColumnWidthSizerMixin):
    def __init__(self, *args, **kw):
        ListCtrlExtended.__init__(self, *args, **kw)
        self._bindColumnSizingEvents()
        self._reflected = ReflectedListEvents(self)

