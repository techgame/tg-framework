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

from TG.w3c.xmlBuilder import ElementBase
from TG.w3c.xmlClassBuilder import XMLFactory

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def invokeRestoreable(elem, elemBuilder, restoreElem, ctxHost=None):
    if ctxHost is not None:
        ctxHost.pushContext(force=1)

    invokename = '::invoke:' + restoreElem.getObject()
    elem.setContextVar(invokename, elem.asWeakProxy())
    restoreElem.restoreChildren(elemBuilder)
    elem.delContextVar(invokename)

    if ctxHost is not None:
        ctxHost.popContext()

class RestoreMixin(object):
    _storedChildren = None
    _storingState = True

    def restoreChildren(self, builder, itemFilter=lambda item: item):
        self.setStoringState(False)
        result = []
        # Emulate the Sub Elements
        for isnode, item, srcref in self.getStoredChildren():
            if isnode: 
                item = itemFilter(item)
                child = self._restoreChild(item, builder, itemFilter=itemFilter)
                result.append(child)
            else: 
                builder._charDataEx(item, srcref)
        return result

    def getStoringState(self):
        return self._storingState
    def setStoringState(self, storing=True):
        self._storingState = storing

    def _restoreChild(self, item, builder, *args, **kw):
        return item.restore(builder, *args, **kw)

    def getStoredChildren(self):
        if self._storedChildren is None:
            self.setStoredChildren([])
        return self._storedChildren
    def setStoredChildren(self, storedChildren):
        self._storedChildren = storedChildren
    def delStoredChildren(self):
        if self._storedChildren is not None:
            del self._storedChildren

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def xmlAddElement(self, elemBuilder, node, elem, srcref):
        if self.getStoringState():
            self.getStoredChildren().append((True, elem, srcref))
        else:
            self.__super.xmlAddElement(elemBuilder, node, elem, srcref)
    def xmlAddData(self, elemBuilder, data, srcref): 
        if self.getStoringState():
            self.getStoredChildren().append((False, data, srcref))
        else:
            self.__super.xmlAddData(elemBuilder, data, srcref)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _createXMLFactories(klass, namespace):
        klass.xmlFactories = XMLFactory.Collection({
            (namespace, klass.__name__): XMLFactory.Static(klass),
            None: XMLFactory.Static(StoreXML),
        }).setName(klass.__name__)
        return klass.xmlFactories
    _createXMLFactories = classmethod(_createXMLFactories)
RestoreMixin._RestoreMixin__super = super(RestoreMixin)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ElementRestoreMixin(RestoreMixin):
    settingName = '::settings'
    filteredSettings = ['ctxobj', 'ctxelem', 'unravel', 'unravel-stop']

    def saveSettingsInContext(self):
        items = self._settings.items()
        result = [i for i in items if i[0] not in self.filteredSettings]
        self.setContextVar(self.settingName, dict(result))
    def removeSettingsInContext(self):
        try: self.delContextVar(self.settingName)
        except AttributeError: pass

    invokeRestoreable = invokeRestoreable

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class StoreXML(RestoreMixin, ElementBase):
    def __init__(self, builder, xmlParent, node, attributes, namespacemap): 
        self.xmlParent = lambda: xmlParent
        self.node, self.attributes, self.namespacemap = node, attributes, namespacemap

    def __repr__(self):
        return '<%s.%s element: %r attrs: %r>' % (self.__class__.__module__, self.__class__.__name__, 
                self.node[1], self.attributes)

    def restore(self, builder, children=None, *args, **kw):
        # Emulate the namespace start calls
        for uri, prefix in self.namespacemap.iterxmlns(False):
            builder._startNamespaceDeclHandler(prefix, uri)

        # Emulate the Start of an element
        name = builder.seperator.join(self.node)
        result = builder._startElementEx(name, self.attributes, self.attributes.srcref)

        self.restoreChildren(builder, *args, **kw)

        # Emulate the End of an element
        builder._endElement(name)

        # Emulate the namespace end calls
        for uri, prefix in self.namespacemap.iterxmlns(False):
            builder._endNamespaceDeclHandler(prefix)

        return result

    def xmlInitStarted(self, elemBuilder): pass
    def xmlPreAddElement(self, elemBuilder, name, attributes, srcref): pass
    def xmlPostAddElement(self, elemBuilder, elem): pass
    def xmlInitFinalized(self, elemBuilder): pass
    def xmlBuildComplete(self, elemBuilder): pass
    def xmlGetElement(self, elemBuilder): 
        return self

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class store(StoreXML):
    xmlFactories = XMLFactory.Collection({
        None: XMLFactory.Static(StoreXML),
        }).setName('store')

    def xmlInitStarted(self, elemBuilder):
        elemBuilder.pushXMLFactories(self.xmlFactories)
    def xmlInitFinalized(self, elemBuilder):
        elemBuilder.popXMLFactories()

