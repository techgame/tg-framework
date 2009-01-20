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

import logging
from TG.common.iterators import iterFilteredMapping
from TG.common.contextApply import ContextApply_s_p
from TG.notifications import subject, provider

from menu import ContextMenuTemplate

import defaults

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ContextModel(object):
    """ContextModel provides an access point to ask questions of the current context.

    ContextModel features include:

        * asking the context trace for an action on a specific object

            ctxNode.getAction('select', selectedResource)
            ctxNode.getAction('view', selectedViewFacet)

        * asking the context to build the context menu for a specific object
            
            ctxNode.getMenu(forObject=selectedResource)
            ctxNode.getMenu(None, selectedResource)
            ctxNode.getMenu('short', selectedResource)

    """
    log = logging.getLogger(__name__)

    defaultMenu = defaults.defaultMenu
    defaultHostObject = defaults.defaultHostObject 
    DefaultMenuTemplate = ContextMenuTemplate

    onGetAction = provider.PredicatedProvider.property()
    onGetNewMenuTemplate = provider.PredicatedProvider.property()
    onUpdateMenuTemplate = subject.Subject.property()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    _host = None
    _hostContextRole = defaults.primaryRole
    _nextContext = None

    def __init__(self, host, hostContextRole=defaults.primaryRole):
        self.setHost(host)
        self.setHostContextRole(hostContextRole)

    def __repr__(self):
        role = self.getHostContextRole()
        if role is not None:
            return "<%s.%s role:[%s] for:%r>" % (self.__class__.__module__, self.__class__.__name__, role, self.getHost())
        else:
            return "<%s.%s for:%r>" % (self.__class__.__module__, self.__class__.__name__, self.getHost())

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getHost(self, includeRole=False):
        return self._host
    def setHost(self, host):
        self._host = host

    def getHostContextRole(self):
        return self._hostContextRole
    def setHostContextRole(self, hostContextRole):
        self._hostContextRole = hostContextRole

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getNextContextModel(self):
        if self._nextContext is None:
            return self.getHost().getNextContextModel()
        else:
            return self._nextContext
    def setNextContextModel(self, nextContext):
        self._nextContext = nextContext

    def iterNextContexts(self):
        return self.iterContexts(False)
    def iterContexts(self, includeSelf=True):
        if includeSelf: next = self
        else: next = self.getNextContextModel()

        while next is not None:
            yield next
            next = next.getNextContextModel()

    def printContextTrace(self):
        for next in self.iterContexts():
            print next

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Context Related Queries
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    #~ Actions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def bindAction(self, actionName, forObject=defaultHostObject, **kw):
        forObject = self._contextObject(forObject)
        action = self.findAction(actionName, forObject)
        if action is not None:
            self.log.info("Binding action %r for %r", actionName, forObject)
            return ContextApply_s_p(action, self, forObject, **kw)
        else:
            self.log.info("No action %r found for %r", actionName, forObject)
            return None

    def performAction(self, actionName, forObject=defaultHostObject, evt=None, **kw):
        forObject = self._contextObject(forObject)
        action = self.findAction(actionName, forObject)
        if action is not None:
            self.log.info("Preforming action %r for %r", actionName, forObject)
            return action(self, forObject, evt, **kw)
        else:
            self.log.info("No action %r found for %r", actionName, forObject)
            return None

    def findAction(self, actionName, forObject=defaultHostObject):
        """Returns a matching action for (actionName, forObject) in the current context.

        An Action is based on the Command Pattern, and therefore is more than
        just a callable object.  This allows lookup and information for the
        context menu implementation, as well as information for buttons.

        Similar to looking up a variable, search progresses from the most
        specific context layer to the most general layer."""
        forObject = self._contextObject(forObject)
        self.log.debug("Finding action %r for %r", actionName, forObject)
        def visit(ctx): 
            return ctx._getAction(actionName, forObject)
        for action in iterFilteredMapping(None, visit, self.iterContexts()):
            return action
        return None
            
    def _getAction(self, actionName, forObject=defaultHostObject):
        """Returns a matching action for (actionName, forObject) locally."""
        for action in self.onGetAction.request(actionName, forObject):
            return action
        return self.getHost()._getContextActionEntry(actionName, self.getHostContextRole())

    #~ Menus ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def popupMenuEvt(self, evt, menuName=defaultMenu, forObject=defaultHostObject):
        menu = self.getMenu(menuName, forObject)
        if menu:
            self.log.info("Showing menu %r for %r", menuName, forObject)
            return menu.popupEvt(evt)
        else:
            self.log.info("No menu %r found for %r", menuName, forObject)

    def popupMenuOn(self, window, position=None, menuName='normal', forObject=defaultHostObject):
        """For position pass an (x,y) tuple, 'window', or 'mouse', or None"""
        menu = self.getMenu(menuName, forObject)
        if menu:
            return menu.popupOn(window, position)

    def getMenu(self, menuName=defaultMenu, forObject=defaultHostObject):
        """Returns a built context menu for (menuName, forObject) in the current context"""
        forObject = self._contextObject(forObject)
        self.log.debug("Getting menu %r for %r", menuName, forObject)
        menuTemplate = self.findMenuTemplate(menuName, forObject)
        return menuTemplate.getMenu()

    def findMenuTemplate(self, menuName=defaultMenu, forObject=defaultHostObject):
        forObject = self._contextObject(forObject)
        def visit(ctx): 
            return ctx._getNewMenuTemplate(menuName, forObject)
        for menuTemplate in iterFilteredMapping(None, visit, self.iterContexts()):
            return self._buildMenuTemplate(menuTemplate, forObject)
        return self._buildMenuTemplate(self.DefaultMenuTemplate(self, forObject), forObject)
            
    def _getNewMenuTemplate(self, menuName, forObject):
        """Returns an instantiated but UN-built context menu template to interact with"""
        for menu in self.onGetNewMenuTemplate.request(menuName, forObject):
            return menu
        return self.getHost().getContextMenuTemplateEntry(menuName, self.getHostContextRole())

    def _buildMenuTemplate(self, menuTemplate, forObject):
        """Dynamically builds the pluggable menu template from the current context"""
        for next in self.iterContexts():
            next._updateMenuTemplate(menuTemplate, forObject)
        return menuTemplate

    def _updateMenuTemplate(self, menuTemplate, forObject):
        self.onUpdateMenuTemplate.update(menuTemplate, forObject)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _contextObject(self, forObject=defaultHostObject):
        if forObject is self.defaultHostObject:
            return self.getHost().getSelectedResource()
        else:
            return forObject

