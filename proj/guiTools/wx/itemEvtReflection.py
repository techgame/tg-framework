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
from TG.guiTools.wx import wxVersion

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ ItemEvtHandlers
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ItemModelBase(object):
    pass

class ItemEvtHandler(wx.EvtHandler, ItemModelBase):
    def processItemEvt(self, evt, item):
        result = self.ProcessEvent(evt)
        return result

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Event Support Convience Mixins
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ItemModelSupportMixin:
    ItemModelFactory = ItemModelBase
    _model = None

    def getItemModel(self):
        if self._model is None:
            self.createItemModel()
        return self._model
    def setItemModel(self, itemModel):
        self._model = itemModel
    def createItemModel(self):
        model = self.ItemModelFactory()
        self.setItemModel(model)
        return model

    def getItemEvtHandler(self, container):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

class ItemEventModelSupportMixin(ItemModelSupportMixin):
    ItemModelFactory = ItemEvtHandler

    def getItemEvtHandler(self, container):
        return self.getItemModel()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Reflected Event Redirectors
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ReflectedEventsBase(object):
    def __init__(self, ctrl=None):
        if ctrl is not None:
            self.setCtrl(ctrl)

    def getCtrl(self):
        return self._ctrl
    def setCtrl(self, ctrl):
        self._ctrl = ctrl
        self._hookItemEvents(ctrl, ctrl.GetId())

    def _hookItemEvents(self, ctrl, ctrlId):
        raise NotImplementedError("SubclassResponsibility")

    def _delegateEventToSink(self, evt, evtSink, item):
        if hasattr(evtSink, 'processItemEvt'):
            evtSink.processItemEvt(evt, item)
        else: 
            evt.Skip()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ReflectedListEvents(ReflectedEventsBase):
    def _hookItemEvents(self, listCtrl, listId):
        wx.EVT_LIST_BEGIN_DRAG(listCtrl, listId, self._onListItemEvent)
        wx.EVT_LIST_BEGIN_RDRAG(listCtrl, listId, self._onListItemEvent)
        #XXX: where is wx.EVT_LIST_END_DRAG(listCtrl, listId, self._onListItemEvent)

        wx.EVT_LIST_BEGIN_LABEL_EDIT(listCtrl, listId, self._onListItemEvent)
        wx.EVT_LIST_END_LABEL_EDIT(listCtrl, listId, self._onListItemEvent)

        wx.EVT_LIST_DELETE_ITEM(listCtrl, listId, self._onListItemEvent)

        wx.EVT_LIST_ITEM_SELECTED(listCtrl, listId, self._onListItemEvent)
        wx.EVT_LIST_ITEM_DESELECTED(listCtrl, listId, self._onListItemEvent)
        wx.EVT_LIST_ITEM_ACTIVATED(listCtrl, listId, self._onListItemEvent)
        wx.EVT_LIST_ITEM_FOCUSED(listCtrl, listId, self._onListItemEvent)
        wx.EVT_LIST_ITEM_MIDDLE_CLICK(listCtrl, listId, self._onListItemEvent)
        wx.EVT_LIST_ITEM_RIGHT_CLICK(listCtrl, listId, self._onListItemEvent)

        wx.EVT_LIST_KEY_DOWN(listCtrl, listId, self._onListItemEvent)

        # well... columns are really items in wx... soooo...
        wx.EVT_LIST_COL_CLICK(listCtrl, listId, self._onListColumnEvent)
        wx.EVT_LIST_COL_RIGHT_CLICK(listCtrl, listId, self._onListColumnEvent)

        wx.EVT_LIST_COL_BEGIN_DRAG(listCtrl, listId, self._onListColumnEvent)
        wx.EVT_LIST_COL_DRAGGING(listCtrl, listId, self._onListColumnEvent)
        wx.EVT_LIST_COL_END_DRAG(listCtrl, listId, self._onListColumnEvent)

    def _onListItemEvent(self, evt):
        evtObj = evt.GetEventObject()
        item = evt.GetItem()
        if not item:
            item = evtObj.GetFirstSelected()

        evtSink = evtObj.getItemEvtHandler(item)
        self._delegateEventToSink(evt, evtSink, item)

    def _onListColumnEvent(self, evt):
        evtObj = evt.GetEventObject()
        item = evt.GetItem()
        # correct the column of the item from evt.GetColumn
        item.SetColumn(evt.GetColumn()) # why?

        evtSink = evtObj.getColumnItemEvtHandler(item)
        self._delegateEventToSink(evt, evtSink, item)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ReflectedTreeEvents(ReflectedEventsBase):
    def _hookItemEvents(self, treeCtrl, treeId):
        wx.EVT_TREE_BEGIN_DRAG(treeCtrl, treeId, self._onTreeItemEvent)
        wx.EVT_TREE_BEGIN_RDRAG(treeCtrl, treeId, self._onTreeItemEvent)
        wx.EVT_TREE_END_DRAG(treeCtrl, treeId, self._onTreeItemEvent)

        wx.EVT_TREE_BEGIN_LABEL_EDIT(treeCtrl, treeId, self._onTreeItemEvent)
        wx.EVT_TREE_END_LABEL_EDIT(treeCtrl, treeId, self._onTreeItemEvent)

        wx.EVT_TREE_DELETE_ITEM(treeCtrl, treeId, self._onTreeItemEvent)

        wx.EVT_TREE_GET_INFO(treeCtrl, treeId, self._onTreeItemEvent)
        wx.EVT_TREE_SET_INFO(treeCtrl, treeId, self._onTreeItemEvent)

        wx.EVT_TREE_ITEM_ACTIVATED(treeCtrl, treeId, self._onTreeItemEvent)
        wx.EVT_TREE_ITEM_COLLAPSED(treeCtrl, treeId, self._onTreeItemEvent)
        wx.EVT_TREE_ITEM_COLLAPSING(treeCtrl, treeId, self._onTreeItemEvent)

        wx.EVT_TREE_ITEM_EXPANDED(treeCtrl, treeId, self._onTreeItemEvent)
        wx.EVT_TREE_ITEM_EXPANDING(treeCtrl, treeId, self._onTreeItemEvent)

        wx.EVT_TREE_SEL_CHANGED(treeCtrl, treeId, self._onTreeItemEvent)
        wx.EVT_TREE_SEL_CHANGING(treeCtrl, treeId, self._onTreeItemEvent)

        wx.EVT_TREE_ITEM_RIGHT_CLICK(treeCtrl, treeId, self._onTreeItemEvent)
        wx.EVT_TREE_ITEM_MIDDLE_CLICK(treeCtrl, treeId, self._onTreeItemEvent)

        wx.EVT_TREE_KEY_DOWN(treeCtrl, treeId, self._onTreeItemEvent)

        if wxVersion() >= '2.5':
            wx.EVT_TREE_ITEM_GETTOOLTIP(treeCtrl, treeId, self._onTreeItemEvent)

    def _onTreeItemEvent(self, evt):
        evtObj = evt.GetEventObject()
        item = evt.GetItem() or evtObj.GetSelection() or None
        evtSink = evtObj.getItemEvtHandler(item)
        self._delegateEventToSink(evt, evtSink, item)

