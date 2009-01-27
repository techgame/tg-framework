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
from TG.guiTools.wx.sizerTools import adjustLayoutContainerSizes, HostLayoutLink
from TG.notifications.event import ObjectEvent

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class _matchany(object):
    def __eq__(self, other): return True
    def __ne__(self, other): return False
_matchany = _matchany()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class DockContainerBase(object):
    onDockedTo = ObjectEvent.objProperty() #(dockcontainer, dockHost, redocking)
    onUndockedFrom = ObjectEvent.objProperty() #(dockcontainer, dockHost, redocking)
    _dockHost = None
    _isDocked = False
    _model = None

    def __init__(self, dockHost=None):
        self.setDockHost(dockHost)
        self.dock()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ DockHost
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getDockHost(self):
        return self._dockHost
    def setDockHost(self, dockHost):
        self._dockHost = dockHost

    def onDockToHost(self, dockHost, dockItem):
        pass
    def onUndockFromHost(self, dockHost, dockItem):
        pass

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Model Accessors
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getModel(self):
        return self._model
    def setModel(self, model):
        self._model = model

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Dock Items
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def iterDockItems(self):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ IsDocked
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def isDocked(self, dockedTo=None):
        if not self.getIsDocked():
            # The state variable says we are not docked
            return False
        elif dockedTo is None:
            # if dockedTo is None, we are docked if we have a valid dockhost
            return (self.getDockHost() is not None)
        elif dockedTo is self.getDockHost():
            # since dockedTo is not None, we are docked if the dockedTo is the
            # current dockHost.  Answer True to the qualified question
            return True
        else:
            # We are not currently docked because either the current dockHost
            # is None or it is not the one that was specified in 'dockedTo'
            return False

    def getIsDocked(self):
        """Use isDocked() if you want the computed answer"""
        return self._isDocked
    def setIsDocked(self, isDocked):
        self._isDocked = isDocked and (self.getDockHost() is not None)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Container docking interface
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def dockToggle(self):
        """Undock if we are docked.  Dock if we are undocked."""
        if not self.isDocked():
            return self.dock()
        else: 
            return self.undock()

    def dockTo(self, dockHost):
        """Docks the contents of this container to 'dockHost'"""
        if dockHost is not self.getDockHost():
            redocking = dockHost is not None
            self.undock(redocking=redocking)
            self.setDockHost(dockHost)
            if dockHost:
                self.dock(redocking=redocking)
        else:
            self.dock()

    def undockFrom(self, dockHost):
        """Docks the contents of this container to 'dockHost'"""
        if dockHost is self.getDockHost():
            self.undock()

    def dock(self, adjust=True, redocking=None):
        if not self.isDocked() and self.getDockHost() is not None:
            self._dockContainedItems(adjust)
            self.setIsDocked(True)
            self.onDockedTo(self.getDockHost(), redocking)
        elif adjust: 
            self._adjustContainedItems()
            self.setIsDocked(True)

    def undock(self, adjust=True, redocking=None):
        if self.isDocked() and self.getDockHost() is not None:
            self._undockContainedItems()
            self.setIsDocked(False)
            self.onUndockedFrom(self.getDockHost(), redocking)
        elif adjust: 
            self._adjustContainedItems()
            self.setIsDocked(False)
        else:
            # make sure the isDocked variable is False
            self.setIsDocked(True)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Protected implemnetation
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _dockContainedItems(self, adjust=True):
        dockHost = self.getDockHost()
        if adjust: 
            for item, args, kw in self.iterDockItems():
                item.SetSize(item.GetBestSize())
                item.Show(True)
                dockHost.dockItem(self, item, *args, **kw)
        else:
            for item, args, kw in self.iterDockItems():
                dockHost.dockItem(self, item, *args, **kw)

    def _undockContainedItems(self, adjust=True):
        dockHost = self.getDockHost()
        if adjust: 
            for item, args, kw in self.iterDockItems():
                item.SetSize(item.GetBestSize())
                dockHost.undockItem(self, item)
                item.Show(False)
        else:
            for item, args, kw in self.iterDockItems():
                dockHost.undockItem(self, item)

    def _adjustContainedItems(self):
        # make sure everything is hidden
        for item, args, kw in self.iterDockItems():
            item.SetSize(item.GetBestSize())
        self.getDockHost().Layout()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class DockContainer(DockContainerBase):
    """This class is implemented with the same interface as a wx.Sizer so that the skinning framework can treat it like such"""
    _dockItems = None

    def iterDockItems(self):
        return iter(self.getDockItems())

    def getDockItems(self):
        if self._dockItems is None:
            self._dockItems = []
        return self._dockItems

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ wx.Sizer interface 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def GetItem(self, item):
        return None

    def Add(self, item, *args, **kw):
        return self.getDockItems().append((item, args, kw))

    def Prepend(self, item, *args, **kw):
        return self.getDockItems().insert(0, (item, args, kw))

    def Remove(self, item, *args, **kw):
        try: 
            self.getDockItems().remove((item, _matchany, _matchany))
            return True
        except ValueError: 
            return False

    def SetItemMinSize(self, *args, **kw):
        pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ DockHosts
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class DockHostBase(object):
    onDockItem = ObjectEvent.objProperty() #(dockHost, dockcontainer, dockItem)
    onUndockItem = ObjectEvent.objProperty() #(dockHost, dockcontainer, dockItem)

    _onUpdateHandlerMap = None
    _dockContainers = None
    _dockLimit = None
    _model = None

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Model Accessors
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __nonzero__(self):
        model = self.getModel()
        return (model or model is None) and bool(self.getParent())

    def getModel(self):
        return self._model
    def setModel(self, model):
        self._model = model

    def getParent(self):
        return self._parent
    def setParent(self, parent):
        self._parent = parent
    parent = property(getParent, setParent)

    def addUpdateHandler(self, itemKey, itemCallback):
        if self.onUpdateInfoMap is None:
            self.onUpdateInfoMap = {}
        self._onUpdateHandlerMap[itemKey] = itemCallback
    def removeUpdateHandler(self, itemKey):
        self._onUpdateHandlerMap.pop(itemKey)

    def updateItem(self, itemKey, itemValue):
        if not self._onUpdateHandlerMap:
            return

        itemCB = self._onUpdateHandlerMap.get(itemKey)
        if itemCB is None:
            itemCB = self._onUpdateHandlerMap.get(None)

        if itemCB is not None:
            return itemCB(itemKey, itemValue)
        else:
            return False

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ DockHost primary interface
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def dock(self, container):
        container.dockTo(self)

    def dockItem(self, container, dockItem=None, *args, **kw):
        """If dockItem is provided, dock that item to this host.  Otherwise, call container.dockTo(self)"""
        if dockItem is None:
            self.dock(container)
        else:
            self._preDockItem(container, dockItem)
            self._dockItemEx(container, dockItem, *args, **kw)
            self._postDockItem(container, dockItem)

    def undockItem(self, container, dockItem=None):
        """If dockItem is provided, undock that item from this host.  Otherwise, call container.undockFrom(self)"""
        if dockItem is None:
            container.undockFrom(self)
        else:
            self._preUndockItem(container, dockItem)
            self._undockItemEx(container, dockItem)
            self._postUndockItem(container, dockItem)

    def undockAll(self):
        for dockItem in self.getDockContainers():
            self.undockItem(dockItem)

    def undockOne(self, limit=None):
        for dockItem in self.getDockContainers():
            self.undockItem(dockItem)
            break

    def undockToLimit(self, limit=NotImplemented, offset=0):
        if limit is NotImplemented:
            limit = self.getDockLimit()

        if limit is None:
            return
        elif limit < 0:
            limit = max(0, self.getDockedCount() + limit)

        for dockItem in self.getDockContainers():
            if limit < (offset + self.getDockedCount()):
                self.undockItem(dockItem)
            else:
                break

    #~ protected composed method parts ~~~~~~~~~~~~~~~~~~

    def _preDockItem(self, container, dockItem):
        """Part of the dockItem composed method"""
        self.undockToLimit(offset=1)

    def _postDockItem(self, container, dockItem):
        """Part of the dockItem composed method.  Does the common managmenet of
        the dock containers collection, as well as invoking the layout call"""
        self._addItemToContainer(container, dockItem)
        #print "POST DOCK ITEM"
        self.Layout()
        #print 'after layout'
        self.onDockItem(container, dockItem)

    def _preUndockItem(self, container, dockItem):
        """Part of the undockItem composed method"""

    def _postUndockItem(self, container, dockItem):
        """Part of the undockItem composed method.  Does the common managmenet
        of the dock containers collection, as well as invoking the layout
        call"""
        self._removeItemFromContainer(container, dockItem)
        self.Layout()
        self.onUndockItem(container, dockItem)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Dock Containers Collection
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getDockLimit(self):
        return self._dockLimit
    def setDockLimit(self, dockLimit):
        self._dockLimit = dockLimit

    def getDockedCount(self):
        return len(self.getDockContainers())

    def getDockContainers(self):
        if self._dockContainers is None:
            self.setDockContainers([])
        return self._dockContainers
    def setDockContainers(self, dockContainers):
        self._dockContainers = dockContainers

    #~ protected composed method parts ~~~~~~~~~~~~~~~~~~

    def _addItemToContainer(self, container, dockItem):
        self.getDockContainers().append(container)
        container.onDockToHost(self, dockItem)

    def _removeItemFromContainer(self, container, dockItem):
        containers = self.getDockContainers()
        while container in containers:
            containers.remove(container)
        container.onUndockFromHost(self, dockItem)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Subclass Responsibilities
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def Layout(self):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

    def _dockItemEx(self, container, dockItem, *args, **kw):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

    def _undockItemEx(self, container, dockItem, *args, **kw):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class HideEmptyMixin(object):
    def hideEmpty(self):
        hideEmptyObj = self.getHideEmptyObj()
        if not hideEmptyObj:
            return
        elif not self.getDockedCount():
            hideEmptyObj.Show(False)
        elif not hideEmptyObj.IsShown():
            hideEmptyObj.Show(True)
            hideEmptyObj.Layout()

    def getHideEmptyObj(self):
        hideEmptyObj = self.getHideEmpty()
        if isinstance(hideEmptyObj, (wx.Window, wx.WindowPtr)):
            return hideEmptyObj
        elif hideEmptyObj:
            return self.parent
        else: 
            return None

    def getHideEmpty(self):
        return self._hideEmpty
    def setHideEmpty(self, hideEmpty):
        self._hideEmpty = hideEmpty

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class DockHost(DockHostBase, HideEmptyMixin):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    onLayingOut = ObjectEvent.objProperty() # dockhost
    onLayoutComplete = ObjectEvent.objProperty() # dockhost
    prepend = False
    _hideEmpty = False

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __init__(self, parent, layout, prepend=False, hideEmpty=False, rootParent=None, rootLayout=None):
        """Creates a new DockHost instance

        Arguments:
            parent          a wxWindow instance for the dockitems to be reparented to
            layout          a layout sizer instance for the dockitems to be added to
            prepend         whether the dockitems should be added to the front or back of the layout sizer
            hideEmpty       if parent (or rootParent) should be hidden if nothing is docked
            rootParent      typically the frame containing 'parent' so that minsize issues can be managed
            rootLayout      typically the layout of the rootParent, so that a refresh can be forced down the chain
        """
        self.setParent(parent)
        self.rootParent = rootParent or parent
        self.layout = layout
        self.rootLayout = rootLayout or layout
        self.prepend = prepend
        self.setHideEmpty(hideEmpty)

    def _dockItemEx(self, container, dockItem, *args, **kw):
        dockItem.Reparent(self.parent)
        if self.prepend:
            sizerItem = self.layout.Prepend(dockItem, *args, **kw)
        else:
            sizerItem = self.layout.Add(dockItem, *args, **kw)
        HostLayoutLink.forLayoutObj(dockItem, self.layout, sizerItem)

    def _undockItemEx(self, container, dockItem, *args, **kw):
        # The following code is not required, but included so 
        # we don't wonder about the asymetry ;)
        ##dockItem.Reparent(None)

        # Disable size hints so the frame can resize when needed
        # We will re-enable in self.Layout
        self.parent.SetSizeHints(0, 0)

        self.layout.Remove(dockItem)

    def Layout(self):
        self.onLayingOut()
        self.hideEmpty()
        self.rootLayout.Layout()
        if self.layout is not self.rootLayout:
            self.layout.Layout()
        self._adjustLayoutContainerSizes()
        self.onLayoutComplete()

        #print "LAYOUT:", self
        #import traceback
        #traceback.print_stack()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Protected Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _adjustLayoutContainerSizes(self):
        adjustLayoutContainerSizes(self.parent, self.layout)

        if (self.rootLayout is not self.layout) or (self.rootParent is not self.parent):
            adjustLayoutContainerSizes(self.rootParent, self.rootLayout)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class NotebookDockHost(DockHostBase, HideEmptyMixin):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    prepend = False
    _hideEmpty = False
    selectpage = True

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Definitions 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    class NotebookDockPage(wx.Panel):
        def __init__(self, *args, **kw):
            wx.Panel.__init__(self, *args, **kw)
            self.dockcontainer = None
            self._dockItem = None
            self.sizer = wx.BoxSizer(wx.VERTICAL)
            self.SetSizer(self.sizer)

        def isDocked(self, dockItem):
            return self._dockItem is dockItem

        def undockItem(self, dockcontainer, dockItem, *args, **kw):
            if self._dockItem is dockItem:
                self.dockItem(None, None)

        def dockItem(self, dockcontainer, dockItem, *args, **kw):
            if self._dockItem is not None:
                self.sizer.Remove(self._dockItem)
            self._dockContainer = dockcontainer
            self._dockItem = dockItem
            if self._dockItem is not None:
                sizerItem = self.sizer.Add(self._dockItem, *args, **kw)
                HostLayoutLink.forLayoutObj(self._dockItem, self.sizer, sizerItem)
            self.Layout()

        def Layout(self):
            self.sizer.Layout()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __init__(self, parent, selectpage=True, prepend=False, hideEmpty=False):
        self.setParent(parent)
        self.selectpage = selectpage
        self.prepend = prepend
        self.setHideEmpty(hideEmpty)
        self._used_pages = []
        self._available_pages = []

    def _dockItemEx(self, container, dockItem, *args, **kw):
        page = self._acquireNotebookDockPage()
        dockItem.Reparent(page)

        page.dockItem(container, dockItem, *args, **kw)
        text = page.GetLabel()

        if self.prepend:
            self.parent.InsertPage(0, page, text, self.selectpage)
        else:
            self.parent.AddPage(page, text, self.selectpage)
        page.Show(True)

    def _undockItemEx(self, container, dockItem, *args, **kw):
        # The following code is not required, but included so 
        # we don't wonder about the asymetry ;)
        ##dockItem.Reparent(None)

        page = self._findNotebookDockPage(dockItem)
        if page is None: raise KeyError, "Dockitem not found"
        page.undockItem(container, dockItem)

        for idx in range(self.parent.GetPageCount()):
            if self.parent.GetPage(idx) is page:
                self.parent.RemovePage(idx)
                break

        self._releaseNotebookDockPage(page)

    def Layout(self):
        self.hideEmpty()

    def _acquireNotebookDockPage(self):
        try:
            result = self._available_pages.pop()
        except IndexError:
            result = self.NotebookDockPage(self.parent, wx.NewId())
            result.Show(False)
        self._used_pages.append(result)
        return result

    def _releaseNotebookDockPage(self, page):
        page.Show(False)
        try: 
            self._used_pages.remove(page)
        except ValueError: 
            pass
        self._available_pages.append(page)

    def _findNotebookDockPage(self, dockItem):
        for page in self._used_pages:
            if page.isDocked(dockItem):
                return page

