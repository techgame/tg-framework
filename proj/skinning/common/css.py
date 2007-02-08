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

import weakref
from TG.w3c import css
from TG.w3c.css import *

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CSSSkinElementInterface(css.CSSElementInterfaceBase):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    xmlParent = lambda self:None
    _children = None
    _inlineStyle = None
    _previousSibling = None
    _nextSibling = None

    _pseudoStateHandlerLookup = {
        'first-child': 
            lambda self: not bool(self.getPreviousSibling()),
        'not-first-child': 
            lambda self: bool(self.getPreviousSibling()),

        'last-child': 
            lambda self: not bool(self.getNextSibling()),
        'not-last-child': 
            lambda self: bool(self.getNextSibling()),

        'middle-child': 
            lambda self: not bool(self.getPreviousSibling()) and not bool(self.getNextSibling()),
        'not-middle-child': 
            lambda self: bool(self.getPreviousSibling()) or bool(self.getNextSibling()),
        }

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Definitions 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __init__(self, host, node, attributes, namespaceMap):
        self.node = node
        self.emptyXmlns = not bool(namespaceMap)
        self.attrs = attributes

    def setXMLParent(self, xmlParent):
        self.xmlParent = xmlParent.asWeakRef()
        if xmlParent.hasChildren():
            previous = xmlParent.getChildren()[-1]
            self.setPreviousSibling(previous.asWeakProxy())
            previous.setNextSibling(self.asWeakProxy())

    def addElement(self, element, srcref):
        element.setXMLParent(self)
        self.getChildren().append(element)

    def getChildren(self):
        if self._children is None:
            self.setChildren([])
        return self._children
    def setChildren(self, children):
        self._children = children
    def hasChildren(self):
        return bool(self._children)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Weakref Utils
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def asWeakRef(self):
        return weakref.ref(self)

    def asWeakProxy(self):
        return weakref.proxy(self)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def matchesNode(self, node):
        if node[1] not in ('*', self.node[1]):
            return False

        if node[0] in (None, '*'):
            # matches any namespace
            return True
        elif node[0] == '':
            # matches when xmlns is empty
            return (not self.emptyXmlns)
        else: # full compare
            return node[0] == self.node[0]

    def getAttr(self, name, default=NotImplemented):
        return self.attrs.get(name, default)
    def getClassAttr(self): 
        return self.getAttr('css-class', None) or self.getAttr('class', '')

    def inPseudoState(self, name, params=()):
        handler = self._pseudoStateHandlerLookup.get(name, lambda self: False)
        return handler(self)

    def iterXMLParents(self, includeSelf=False):
        if includeSelf: 
            current = self
        else: 
            current = self.xmlParent()
        while current is not None:
            yield current
            current = current.xmlParent()

    def getPreviousSibling(self):
        return self._previousSibling
    def setPreviousSibling(self, previousSibling):
        self._previousSibling = previousSibling

    def getNextSibling(self):
        return self._nextSibling
    def setNextSibling(self, nextSibling):
        self._nextSibling = nextSibling

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CSSParser(css.CSSParser):
    xmlBuilder = lambda self: None

    def parseExternal(self, resourceName, cssBuilder=None):
        cssResource = self.getURIResolver().resolve(resourceName)
        try:
            cssFile = cssResource.open('r')
            try:
                result = self.parseFile(cssFile, False)
            finally:
                cssFile.close()
        except CSSParseError, e:
            e.setFilename(cssResource.getPath())
            e.raiseFromSrc()

        return result

    def parseWithSrcRef(self, src, srcRef):
        try:
            result = self.parse(src)
        except CSSParseError, e:
            e.raiseFromSrc(srcRef)

        return result

    def getXMLBuilder(self):
        return self.xmlBuilder()
    def setXMLBuilder(self, xmlBuilder):
        try:
            self.xmlBuilder = xmlBuilder.asWeakRef()
        except (AttributeError, TypeError):
            self.xmlBuilder = lambda: xmlBuilder
        self.xmlnsSynonyms = xmlBuilder.xmlnsSynonyms

    def getContext(self):
        return self.getXMLBuilder().getContext()
    def getContextVar(self, name, *args):
        return getattr(self.getContext(), name, *args)
    def getURIResolver(self):
        return self.getContext().getURIResolver()

