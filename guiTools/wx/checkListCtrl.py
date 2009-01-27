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
from wx.lib.mixins.listctrl import CheckListCtrlMixin
from listColumnSizers import ListColumnWidthSizerMixin
from listCtrl import ListCtrlBase, ListItem, ListColumnItem, ReflectedListEvents
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ ListCtrl related
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CheckListCtrlBase(ListCtrlBase, CheckListCtrlMixin):
    def __init__(self, *args, **kw):
        ListCtrlBase.__init__(self, *args, **kw)
        CheckListCtrlMixin.__init__(self)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CheckListCtrlExtended(CheckListCtrlBase):
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

class CheckListCtrl(CheckListCtrlExtended, ListColumnWidthSizerMixin):
    def __init__(self, *args, **kw):
        CheckListCtrlExtended.__init__(self, *args, **kw)
        self._bindColumnSizingEvents()
        self._reflected = ReflectedListEvents(self)

