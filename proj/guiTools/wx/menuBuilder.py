#!/usr/bin/env python
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##~ Copyright (C) 2002-2004  TechGame Networks, LLC.
##~ 
##~ This library is free software; you can redistribute it and/or
##~ modify it under the terms of the BSD style License as found in the 
##~ LICENSE file included with this distribution.
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# NOTE: These classes intentionally follow FirstUpperCamelCase for methods to
# keep with the wxPython theme

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import wx
from TG.common import contextApply

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MenuItemBase(object):
    def __init__(self, *args, **kw):
        if args or kw:
            self.create(*args, **kw)

    def create(self, *args, **kw):
        raise NotImplementedError("Subclass Responsibility")

    def getId(self):
        try:
            return self.wxid
        except AttributeError:
            self.wxid = wx.NewId()
            return self.wxid

    def asMenuItem(self, menu):
        raise NotImplementedError("Subclass Responsibility")

    def addToMenu(self, menu):
        menu.addItem(self)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MenuItemBaseAdv(MenuItemBase):
    label = ""
    accel = ""
    help = ""
    checkedbmp = wx.NullBitmap
    uncheckedbmp = wx.NullBitmap

    def create(self, label, help=None, accel=None, checkedbmp=None, uncheckedbmp=None, **kw):
        self.setLabel(label)
        self.setHelp(accel)
        self.setAccel(accel)
        if 'bitmap' in kw:
            if checkedbmp is not None: 
                raise ValueError, 'Both bitmap and checkedbmp were specified, conflicting arguments.'
            if uncheckedbmp  is not None: 
                raise ValueError, 'Both bitmap and uncheckedbmp were specified, conflicting arguments.'
            checkedbmp = uncheckedbmp = kw['bitmap']
        self.setBitmaps(checkedbmp, uncheckedbmp)

    def getLabel(self): 
        return self.label
    def setLabel(self, label):
        self.label = label

    def getAccel(self): 
        return self.accel
    def setAccel(self, accel):
        if accel is None:
            try: del self.accel
            except AttributeError: pass
        else:
            self.accel = accel

    def getHelp(self): 
        return self.help
    def setHelp(self, help):
        if help is None:
            try: del self.help
            except AttributeError: pass
        else:
            self.help = help

    def getBitmaps(self):
        return self.checkedbmp, self.uncheckedbmp
    def setBitmaps(self, checkedbmp=None, uncheckedbmp=None):
        self.checkedbmp = checkedbmp or wx.NullBitmap
        self.uncheckedbmp = uncheckedbmp or wx.NullBitmap

    def _setAdvancedWxMenu(self, menuitem):
        if self.accel: 
            menuitem.setAccel(self.getAccel())
        if self.help: 
            menuitem.setHelp(self.getHelp())
        if self.checkedbmp: 
            menuitem.setBitmaps(*self.getBitmaps())
        return menuitem

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Usable classes
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MenuBuilderBase(object):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    _softSeparator = False
    childTypes = (MenuItemBase, wx.Menu, wx.MenuItem)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Definitions 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getChildren(self):
        try:
            return self._children
        except AttributeError:
            self._children = []
            return self._children

    def isPopulated(self):
        try:
            if self._children:
                return True
        except AttributeError:
            pass
        return False

    def addItem(self, item, separate=False):
        self._addChild(item, separate)
        return item

    def group(self, *args, **kw):
        """Adds a new submenu to the menu"""
        result = GroupMenuItem(*args, **kw)
        return self.addGroupAsSubmenu(result)

    def addGroup(self, item, inline=False, separate=None):
        if separate is None: 
            separate = inline
        if inline:
            result = self.addGroupInline(item, separate)
        else:
            result = self.addGroupAsSubmenu(item, separate)
        return result

    def addGroupAsSubmenu(self, groupMenuItem, separate=False):
        if groupMenuItem is not None:
            self._addChild(groupMenuItem, separate)
        return groupMenuItem

    def addGroupInline(self, groupMenuItem, separate=False):
        """Instead of adding a submenu, InlineGroup takes the subitems and
        inserts them into the current menu"""
        if groupMenuItem is not None:
            self._addChild(groupMenuItem, separate, isGroup=True)
        return self

    def submenu(self, *args, **kw):
        result = SubMenuItem(*args, **kw)
        self._addChild(result)
        return result

    def command(self, *args, **kw):
        result = BindableCommandMenuItem(*args, **kw)
        self._addChild(result)
        return result

    def separator(self, *args, **kw):
        # separator is a hardbreak, and thus clears any softSeparator
        self.clearSoftSeparator()
        result = SeparatorMenuItem(*args, **kw)
        self._addChild(result)
        return result
    hardbreak = separator

    def clearSoftSeparator(self):
        self.setSoftSeparator(False)
    def getSoftSeparator(self):
        return self._softSeparator
    def setSoftSeparator(self, value=True):
        self._softSeparator = value

    def softSeparator(self):
        self.setSoftSeparator(True)
    softbreak = softSeparator

    #~ protected ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def iterChildren(self):
        for isGroup, child in self.getChildren():
            if isGroup:
                for childDelegate in child.iterChildren():
                    yield childDelegate
            else:
                yield child

    def _addChild(self, child, separate=False, isGroup=False):
        if self.getSoftSeparator() or separate:
            self.setSoftSeparator()
            if self.getChildren():
                self.separator()

        if self.childTypes and not isinstance(child, self.childTypes):
            raise TypeError("MenuBuilder child is of an unexpected type: %r" % (type(Child),))

        self.getChildren().append((isGroup, child))

        if separate: 
            # can't use hardbreak -- may be last in menu
            self.clearSoftSeparator()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MenuBuilder(MenuBuilderBase):
    RootMenuFactory = wx.Menu
    _rootMenu = None

    def getRootMenu(self):
        if self._rootMenu is None:
            self.setRootMenu(self.RootMenuFactory())
        return self._rootMenu
    def setRootMenu(self, rootMenu):
        self._rootMenu = rootMenu
    def delRootMenu(self):
        if self._rootMenu is not None:
            del self._rootMenu
    rootMenu = property(getRootMenu, setRootMenu, delRootMenu)

    def asMenu(self, rootmenu=None, eventhost=None):
        menu = self.getRootMenu()
        if rootmenu is None:
            rootmenu = menu
        for menuItem in self.iterChildren():
            if not isinstance(menuItem, wx.MenuItem):
                menuItem = menuItem.asMenuItem(menu, rootmenu, eventhost)
            if menuItem is not None:
                menu.AppendItem(menuItem)
        self.delRootMenu()
        return menu

    def popupOn(self, window, position=None, destroy=False):
        if position is None:
            position = window.GetPosition()
        elif isinstance(position, basestring):
            if position=='mouse':
                position = window.ScreenToClient(wx.GetMousePosition())
            elif position=='window':
                position = window.GetPosition()
        menu = self.asMenu()
        try:
            result = window.PopupMenu(menu, position)
        finally:
            if destroy:
                menu.Destroy()
        return result

    def popupEvt(self, evt, defaultPosition='mouse', **kw):
        eo = evt.GetEventObject()
        try: 
            position = evt.GetPosition()
        except AttributeError: 
            position = defaultPosition
        return self.popupOn(eo, position, **kw)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SeparatorMenuItem(MenuItemBase):
    def asMenuItem(self, menu, rootmenu, eventhost=None):
        result = wx.MenuItem(menu, wx.ID_SEPARATOR, kind=wx.ITEM_SEPARATOR)
        return result

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CommandMenuItemBase(MenuItemBaseAdv):
    def getEventCallback(self):
        raise NotImplementedError("Subclass Responsibility")

    def asMenuItem(self, menu, rootmenu, eventhost=None):
        menuitem = wx.MenuItem(menu, self.getId(), self.label, kind=wx.ITEM_NORMAL)
        self._setAdvancedWxMenu(menuitem)
        wx.EVT_MENU(eventhost or rootmenu, self.getId(), self.getEventCallback())
        return menuitem

class CommandMenuItem(CommandMenuItemBase):
    _evtCallback = None
    def getEventCallback(self):
        return self._evtCallback
    def setEventCallback(self, evtCallback):
        self._evtCallback = evtCallback
    evtCallback = property(getEventCallback, setEventCallback)

class BindableCommandMenuItem(contextApply.Bindable, CommandMenuItemBase):
    def getEventCallback(self):
        return self

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SubMenuItem(MenuItemBaseAdv):
    def asMenuItem(self, menu, rootmenu, eventhost=None):
        submenu = self.getMenu()
        if submenu is not None:
            result = wx.MenuItem(menu, self.getId(), self.label, kind=wx.ITEM_NORMAL)
            self._setAdvancedWxMenu(result)

            if not isinstance(submenu, wx.Menu):
                submenu = submenu.asMenu(rootmenu, eventhost)
            result.SetSubMenu(submenu)
            return result
        else:
            return None

    def create(self, label, menu, help=None, accel=None, checkedbmp=None, uncheckedbmp=None, **kw):
        MenuItemBaseAdv.create(self, label, help, accel, checkedbmp, uncheckedbmp, **kw)
        self.setMenu(menu)

    def getMenu(self):
        return self._menu
    def setMenu(self, menu):
        self._menu = menu
    submenu = menu = property(getMenu, setMenu)
    
    def getChildren(self):
        if not isinstance(menu, wx.Menu):
            return menu.getChildren()
        else:
            return menu.getMenuItems()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class GroupMenuItem(MenuItemBaseAdv, MenuBuilder):
    def __init__(self, label="", *args, **kw):
        MenuBuilder.__init__(self)
        MenuItemBaseAdv.__init__(self, label, *args, **kw)

    def asMenuItem(self, menu, rootmenu, eventhost=None):
        result = wx.MenuItem(menu, self.getId(), self.label, kind=wx.ITEM_NORMAL)
        self._setAdvancedWxMenu(result)

        submenu = self.asMenu(rootmenu, eventhost)
        result.SetSubMenu(submenu)
        return result

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Menu(GroupMenuItem):
    pass

