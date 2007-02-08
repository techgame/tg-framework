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

from TG.w3c import css

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CSSDOMElementInterface(css.CSSElementInterfaceBase):
    """An implementation of css.CSSElementInterfaceBase for xml.dom Element Nodes"""

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    style = None

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

    def __init__(self, domElement):
        self.domElement = domElement
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def matchesNode(self, (namespace, tagName)):
        if tagName not in ('*', self.domElement.tagName):
            return False
        if namespace in (None, '', '*'):
            # matches any namespace
            return True
        else: # full compare
            return namespace == self.domElement.namespaceURI

    def getAttr(self, name, default=NotImplemented):
        attrValue = self.domElement.attributes.get(name)
        if attrValue is not None:
            return attrValue.value
        else:
            return default

    def inPseudoState(self, name, params=()):
        handler = self._pseudoStateHandlerLookup.get(name, lambda self: False)
        return handler(self)

    def iterXMLParents(self, includeSelf=False):
        klass = self.__class__
        current = self.domElement
        if not includeSelf: 
            current = current.parentNode
        while (current is not None) and (current.nodeType == current.ELEMENT_NODE):
            yield klass(current)
            current = current.parentNode

    def getPreviousSibling(self):
        sibling = self.domElement.previousSibling
        while sibling:
            if sibling.nodeType == sibling.ELEMENT_NODE:
                return sibling
            else:
                sibling = sibling.previousSibling
        return None
    def getNextSibling(self):
        sibling = self.domElement.nextSibling
        while sibling:
            if sibling.nodeType == sibling.ELEMENT_NODE:
                return sibling
            else:
                sibling = sibling.nextSibling
        return None

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CSSDOMCascadeStrategy(css.CSSCascadeStrategy):
    def _normalizeCSSElement(self, element):
        if not isinstance(elemnet, CSSDOMElementInterface):
            return 
