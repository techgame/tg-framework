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

import defaults
from model import ContextModel

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Constants / Variables / Etc. 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ContextHostBase(object):
    _contextModels = None
    primaryRole = defaults.primaryRole
    ContextModelFactory = ContextModel

    def getContextModel(self, contextRole=primaryRole):
        if self._contextModels is None:
            self._contextModels = {}

        contextModel = self._contextModels.get(contextRole, None)
        if contextModel is None:
            contextModel = self.createContextModelFor(contextRole)

        return contextModel
    def setContextModel(self, contextModel, contextRole=NotImplemented):
        if self._contextModels is None:
            self._contextModels = {}

        if contextRole is NotImplemented:
            contextRole = contextModel.getHostContextRole()

        self._contextModels[contextRole] = contextModel
    contextModel = property(getContextModel, setContextModel)

    def createContextModelFor(self, contextRole=primaryRole):
        contextModel = self.ContextModelFactory(self, contextRole)
        if contextRole is not self.primaryRole:
            nextContextModel = self.getContextModel(self.primaryRole)
            contextModel.setNextContextModel(nextContextModel)

        self.setContextModel(contextModel)
        return contextModel

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getNextContextModel(self):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

    def getSelectedResource(self):
        return None

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ContextHost(ContextHostBase):
    primaryRole = ContextHostBase.primaryRole
    _contextActionMap = None
    _contextMenuMap = None

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getContextActionMap(self):
        if self._contextActionMap is None:
            self._contextActionMap = {}
        return self._contextActionMap
    def _getContextActionEntry(self, actionName, contextRole=primaryRole):
        actionMap = self.getContextActionMap()
        result = actionMap.get((contextRole, actionName), None)
        if result is None:
            result = actionMap.get((self.primaryRole, actionName), None)
        return result
    def addContextAction(self, action, actionName, contextRole=primaryRole):
        actionMap = self.getContextActionMap()
        actionMap[(contextRole, actionName)] = action
    def removeContextAction(self, actionName, contextRole=primaryRole):
        actionMap = self.getContextActionMap()
        actionMap.pop((contextRole, actionName), None)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getContextMenuTemplateMap(self):
        if self._contextMenuMap is None:
            self._contextMenuMap = {}
        return self._contextMenuMap
    def getContextMenuTemplateEntry(self, menuName, contextRole=primaryRole):
        menuTemplateMap = self.getContextMenuTemplateMap()
        result = menuTemplateMap.get((contextRole, menuName), None)
        if result is None:
            result = menuTemplateMap.get((self.primaryRole, menuName), None)
        return result
    def addContextMenuTemplate(self, menuTemplate, menuName, contextRole=primaryRole):
        menuTemplateMap = self.getContextMenuTemplateMap()
        menuTemplateMap[(contextRole, menuName)] = menuTemplate
    def removeContextMenuTemplate(self, menuTemplate, menuName, contextRole=primaryRole):
        menuTemplateMap = self.getContextMenuTemplateMap()
        menuTemplateMap.pop((contextRole, menuName), None)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def performAction(self, actionName, forObject=defaults.defaultHostObject, evt=None, **kw):
        return self.getContextModel().performAction(actionName, forObject, evt, **kw)
    def popupMenuEvt(self, evt, menuName=defaults.defaultMenu, forObject=defaults.defaultHostObject):
        return self.getContextModel().popupMenuEvt(evt, menuName, forObject)
    def popupMenuOn(self, window, position=None, menuName='normal', forObject=defaults.defaultHostObject):
        return self.getContextModel().popupMenuOn(window, position, menuName, forObject)

