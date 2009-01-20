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
from itemEvtReflection import ReflectedTreeEvents, ItemEventModelSupportMixin

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TreeItemBase(object):
    treeId = None
    parentTreeId = None
    text = ''
    hasChildren = None
    bold = False
    font = None
    bgColour = None
    fgColour = None
    data = None
    imageIndexes = {}
    imageSelectedIdx = -1

    _allImageIds = (wx.TreeItemIcon_Normal, wx.TreeItemIcon_Selected, wx.TreeItemIcon_Expanded, wx.TreeItemIcon_SelectedExpanded)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def setValues(self, text=None, imageIdx=None, imageSelectedId=None, font=None, fgColor=None, bgColor=None, data=None):
        if text is not None:
            self.SetText(text)

        if imageIdx is not None:
            self.SetImage(imageIdx)
        if imageSelectedId is not None:
            self.SetImageSelected(imageSelectedId)

        if font is not None:
            self.SetFont(font)
        if fgColor is not None:
            self.SetTextColour(fgColor)
        if bgColor is not None:
            self.SetBackgroundColour(bgColor)

        if data is not None:
            self.SetData(data)

        self.SetStateMask(mask)

    def GetTreeId(self):
        return self.treeId
    def SetTreeId(self, treeId):
        self.treeId = treeId

    def GetParentTreeId(self):
        return self.parentTreeId
    def SetParentTreeId(self, parentTreeId):
        self.parentTreeId = parentTreeId

    def GetData(self):
        return self.data
    def SetData(self, data):
        self.data = data

    def GetText(self):
        return unicode(self.text)
    def SetText(self, text):
        self.text = text

    def GetImages(self):
        return self.imageIndexes
    def ClearImages(self):
        if self.imageIndexes:
            del self.imageIndexes
    def GetImage(self, key=wx.TreeItemIcon_Normal):
        return self.imageIndexes.get(key, -1)
    def SetImage(self, imageIdx, key=wx.TreeItemIcon_Normal):
        if not self.imageIndexes:
            self.imageIndexes = {}
        self.imageIndexes[key] = imageIdx

    def GetImageSelected(self):
        return self.GetImage(wx.TreeItemIcon_Selected)
    def SetImageSelected(self, imageSelectedIdx):
        self.SetImage(imageSelectedIdx, wx.TreeItemIcon_Selected)

    def GetHasChildren(self):
        return self.hasChildren
    def SetHasChildren(self, hasChildren=True):
        self.hasChildren = hasChildren

    def GetBold(self):
        return self.bold
    def SetBold(self, bold):
        self.bold = bold

    def GetFont(self):
        return self.font
    def SetFont(self, font):
        self.font = font

    def GetTextColour(self):
        return self.fgColour
    GetForegroundColour = GetTextColour
    def SetTextColour(self, fgColour):
        self.fgColour = fgColour
    SetForegroundColour = SetTextColour

    def GetBackgroundColour(self):
        return self.bgColour
    def SetBackgroundColour(self, bgColour):
        self.bgColour = bgColour

    def addToTree(self, treeWin, parent=None):
        if parent:
            self.SetParentTreeId(parent.GetTreeId())
        else: self.SetParentTreeId(None)

        treeId = treeWin.addTreeItemEx(self, self.GetParentTreeId(), self.GetText())
        self.SetTreeId(treeId)

        self.updateToTree(treeWin)
        return self.GetTreeId()

    def updateToTree(self, treeWin):
        treeid = self.GetTreeId()

        treeWin.SetItemText(treeid, self.GetText())

        treeWin.SetItemBold(treeid, self.GetBold())
        font = self.GetFont()
        if font: 
            treeWin.SetItemFont(treeid, font)
        bgColour = self.GetBackgroundColour()
        if bgColour: 
            treeWin.SetItemBackgroundColour(treeid, bgColour)
        fgColour = self.GetTextColour()
        if fgColour: 
            treeWin.SetItemTextColour(treeid, fgColour)

        for key, image in self.GetImages().items():
            treeWin.SetItemImage(treeid, image, key)

        hasChildren = self.GetHasChildren()
        if hasChildren is not None:
            treeWin.SetItemHasChildren(treeid, hasChildren)

        return self

    def fromTree(klass, treeWin, treeid):
        return klass().updateFromTree(treeWin, treeid)
    fromTree = classmethod(fromTree)

    def updateFromTree(self, treeWin, treeid=None):
        if treeid is None:
            treeid = self.GetTreeId()

        self.SetText(treeWin.GetItemText(treeid))
        self.SetBold(treeWin.GetItemBold(treeid))
        self.SetFont(treeWin.GetItemFont(treeid))
        self.SetBackgroundColour(treeWin.GetItemBackgroundColour(treeid))
        self.SetTextColour(treeWin.GetItemTextColour(treeid))

        for key in self._allImageIds:
            imageIdx = treeWin.GetItemImage(treeid, key)
            self.SetImage(imageIdx, key)

        #self.SetData(treeWin.GetPyData(treeid))
        return self

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TreeItem(TreeItemBase, ItemEventModelSupportMixin):
    def addToTree(self, treeWin, parent=None):
        TreeItemBase.addToTree(self, treeWin, parent=parent)
        self.installItemModel(treeWin)

    def installItemModel(self, treeWin):
        treeWin.SetPyData(self.GetTreeId(), self)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ TreeCtrl related
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TreeCtrlMixin:
    TreeItemFactory = TreeItemBase
    if hasattr(wx, 'TreeItemIdPtr'):
        TreeItemClasses = wxClasses(wx.TreeItemId, wx.TreeItemIdPtr)
    else: TreeItemClasses = wxClasses(wx.TreeItemId)

    def getItemModel(self, treeItemId):
        if not treeItemId: return None
        if isinstance(treeItemId, self.TreeItemClasses):
            treeItemId = self.GetPyData(treeItemId)
        return treeItemId.getItemModel()

    def getItemEvtHandler(self, treeItemId):
        if not treeItemId: return None
        if isinstance(treeItemId, self.TreeItemClasses):
            treeItemId = self.GetPyData(treeItemId)
        if treeItemId:
            getItemEvtHandler = getattr(treeItemId, 'getItemEvtHandler', lambda eh: None)
            return getItemEvtHandler(self)
        return None

    def addItem(self, parent=None, *args, **kw):
        ti = self.TreeItemFactory()
        ti.setValues(*args, **kw)
        ti.addToTree(self, parent)
        return ti

    def addTreeItem(self, treeitem, *args, **kw):
        try:
            return treeitem.addToTree(self, *args, **kw)
        except AttributeError:
            return self.addTreeItemEx(treeitem, *args, **kw)

    def addTreeItemEx(self, treeitem, parent=None, *args, **kw):
        if parent:
            itemid = self.AppendItem(parent, *args, **kw)
        else:
            itemid = self.AddRoot(*args, **kw)
        return itemid

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TreeCtrlBase(wx.TreeCtrl, TreeCtrlMixin):
    def ClearAll(self):
        self.clearAllPyData()
        return wx.ListCtrl.ClearAll(self)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TreeCtrl(TreeCtrlBase):
    TreeItemFactory = TreeItem

    def __init__(self, *args, **kw):
        TreeCtrlBase.__init__(self, *args, **kw)
        self._reflected = ReflectedTreeEvents(self)

