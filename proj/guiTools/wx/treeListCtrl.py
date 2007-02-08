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
import wx.gizmos

from itemEvtReflection import ReflectedTreeEvents, ItemEventModelSupportMixin, ItemEventModelSupportMixin, ItemEvtHandler
import treeCtrl

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ TreeListItems
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TreeListItemBase(treeCtrl.TreeItemBase):
    pass

class TreeListItem(TreeListItemBase, ItemEventModelSupportMixin):
    def addToTree(self, treeWin, parent=None):
        TreeItemBase.addToTree(self, treeWin, parent=parent)
        self.installItemModel(treeWin)

    def installItemModel(self, treeWin):
        treeWin.SetPyData(self.GetTreeId(), self)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TreeColumnItem(wx.gizmos.TreeListColumnInfo, ItemEventModelSupportMixin):
    GetAlign = wx.gizmos.TreeListColumnInfo.GetAlignment
    SetAlign = wx.gizmos.TreeListColumnInfo.SetAlignment

    GetMask = lambda *a: None
    SetMask = lambda *a: None

    getProportion = lambda *a: None
    setProportion = lambda *a: None

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

    def addToList(self, treeListCtrl, index=None, column=None):
        if column is not None:
            self.SetColumn(column)
        treeListCtrl.addListColumn(self, self.GetColumn())

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def fromFromList(klass, treeListCtrl, itemid):
        result = treeListCtrl.GetItem(itemid)
        result.__class__ = klass
        return result
    fromFromList = classmethod(fromFromList)

    def updateToList(self, treeListCtrl):
        treeListCtrl.SetItem(self)
        return self

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    _column = 0
    def GetColumn(self):
        return self._column
    def SetColumn(self, column):
        self._column = column

    proportion = 0
    def getProportion(self):
        return self.proportion
    def setProportion(self, proportion):
        self.proportion = proportion

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ TreeListCtrl Releated
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TreeListCtrlMixin(treeCtrl.TreeCtrlMixin):
    TreeItemFactory = TreeListItemBase

    def addListColumn(self, lc, column):
        columnCount = self.GetColumnCount()
        if column < columnCount:
            self.SetColumn(column, lc)
        elif column >= columnCount:
            self.AddColumnInfo(lc)
        else:
            pass #self.InsertColumnInfo(column, lc)


class TreeListCtrlBase(wx.gizmos.TreeListCtrl, TreeListCtrlMixin):
    pass

class TreeListCtrl(TreeListCtrlBase):
    TreeItemFactory = TreeListItemBase

    def __init__(self, *args, **kw):
        TreeListCtrlBase.__init__(self, *args, **kw)
        self._reflected = ReflectedTreeEvents(self)

