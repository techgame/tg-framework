##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~ Copyright (C) 2002-2005  TechGame Networks, LLC.              ##
##~                                                               ##
##~ This library is free software; you can redistribute it        ##
##~ and/or modify it under the terms of the BSD style License as  ##
##~ found in the LICENSE file included with this distribution.    ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from TG.guiTools.wx import menuBuilder

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ContextMenuTemplateAbstract(object):
    _ctxObject = None
    _ctxModel = None

    def __init__(self, contextModel, contextObject):
        self.setContextModel(contextModel)
        self.setContextObject(contextObject)

    def getContextModel(self):
        return self._ctxModel
    def setContextModel(self, ctxModel):
        self._ctxModel = ctxModel

    def getContextObject(self):
        return self._ctxObject
    def setContextObject(self, ctxObject):
        self._ctxObject = ctxObject

    def addActions(self, *actionName, **kw):
        """default=False"""
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def addPostActions(self, *actionNames):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def addObjectMenu(self, objMenuName, objMenu):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def addHostMenu(self, hostMenuName, hostMenu):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ContextMenuTemplateBase(ContextMenuTemplateAbstract):
    builder = menuBuilder
    _ctxObjectMenu = None

    _preActions = ()
    _postActions = ()
    _objectMenus = ()
    _hostMenus = ()

    def getContextObjectMenu(self):
        return self._ctxObjectMenu
    def setContextObjectMenu(self, ctxObjectMenu):
        self._ctxObjectMenu = ctxObjectMenu

    def getPreActions(self):
        if not self._preActions:
            self._preActions = []
        return self._preActions
    def iterPreActions(self):
        return iter(self._preActions)

    def getPostActions(self):
        if not self._postActions:
            self._postActions = []
        return self._postActions
    def iterPostActions(self):
        return iter(self._postActions)

    def getObjectMenus(self):
        if not self._objectMenus:
            self._objectMenus = []
        return self._objectMenus
    def iterObjectMenus(self):
        return iter(self._objectMenus)

    def getHostMenus(self):
        if not self._hostMenus:
            self._hostMenus = []
        return self._hostMenus
    def iterHostMenus(self):
        return iter(self._hostMenus)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def addActions(self, *actionNames, **kw):
        """default keyword inserts the actions at the front"""
        default = kw.pop('default', False)
        preActions = self.getPreActions()
        if default:
            preActions[0:0] = actionNames
        else:
            preActions.extend(actionNames)

    def addPostActions(self, *actionNames):
        postActions = self.getPostActions()
        postActions.extend(actionNames)

    def addObjectMenu(self, objMenuName, objMenu):
        if objMenuName:
            objMenu = self.builder.SubMenuItem(objMenuName, objMenu)
        self.getObjectMenus().append(objMenu)

    def addHostMenu(self, hostMenuName, hostMenu):
        if hostMenuName:
            hostMenu = self.builder.SubMenuItem(hostMenuName, hostMenu)
        self.getHostMenus().append(hostMenu)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ContextMenuTemplate(ContextMenuTemplateBase):
    builder = ContextMenuTemplateBase.builder
    RootMenuFactory = builder.Menu
    _rootMenu = None

    def getRootToolkitMenu(self):
        return self.getRootMenu().getRootMenu()
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

    def getMenu(self):
        menu = self.getRootMenu()
        self.buildMenuActions(menu)
        menu.softSeparator()
        self.buildMenuContext(menu)
        menu.softSeparator()
        self.buildMenuObjects(menu)
        menu.softSeparator()
        self.buildMenuHosts(menu)
        menu.softSeparator()
        self.buildMenuPostActions(menu)

        self.delRootMenu()
        return menu

    def buildMenuActions(self, menu):
        for actionName in self.iterPreActions():
            action = self.getContextModel().bindAction(actionName, self.getContextObject())
            # Note: Temporary
            menu.command(actionName).bind_p(action)
            #if action is not None:
            #    menu.addItem(action.getMenuItem())

    def buildMenuContext(self, menu):
        contextObjMenu = self.getContextObjectMenu()
        menu.addGroup(contextObjMenu, inline=True)

    def buildMenuObjects(self, menu):
        for objMenu in self.iterObjectMenus():
            menu.addGroup(objMenu)

    def buildMenuHosts(self, menu):
        for objMenu in self.iterHostMenus():
            menu.addGroup(objMenu)

    def buildMenuPostActions(self, menu):
        for actionName in self.iterPostActions():
            action = self.getContextModel().bindAction(actionName, self.getContextObject())
            # Note: Temporary
            if actionName[0].islower():
                # we'd use capitalize, except for that it mangles camel case
                actionName = actionName[0].upper() + actionName[1:]
            menu.command(actionName).bind_p(action)
            #if action is not None:
            #    menu.addItem(action.getMenuItem())

