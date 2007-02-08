#!/usr/bin/env python
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##~ Copyright (C) 2002-2004  TechGame Networks, LLC.
##~ 
##~ This library is free software; you can redistribute it and/or
##~ modify it under the terms of the BSD style License as found in the 
##~ LICENSE file included with this distribution.
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""Abstract base classes for building Python object trees from an XML stream."""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports                                           
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import weakref
from timeit import default_timer as systemTimer

from xmlNamespaceMap import XMLNamespaceMap
from xmlParserContext import ExpatParserCmd

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ElementFactoryError(Exception):
    def __init__(self, message, builder=None):
        self.message = message
        if builder is not None:
            self.srcref = builder.getSourceFilenameAndLineNumber()
        else:
            self.srcref = '<unknown>'

    def __str__(self):
        return '%s in %s' % (self.srcref, self.message)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Element Stack definition
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ElementStackAbstract(object):
    topOffset = -1

    def __init__(self, builder, stack=None):
        self.setBuilder(builder)
        if stack is None: self.stack = []
        else: self.stack = stack

    def __len__(self): 
        return len(self.stack)

    def saveState(self):
        return self.__class__(self.getBuilder(), self.stack[:])

    def topElementOrNone(self):
        if self.stack:
            return self.stack[self.topOffset]
        else: return None

    def topElement(self):
        return self.stack[self.topOffset]

    def getElement(self, idx=-1, wrapped=True):
        element = self.stack[idx]
        if wrapped:
            return element.xmlGetElement(self)
        else: return element
    __getitem__ = getElement

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getBuilder(self):
        return self.xmlBuilder()
    def setBuilder(self, xmlBuilder):
        self.xmlBuilder = xmlBuilder.asWeakRef()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def buildElement(node, attributes, namespacemap):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def push(self, element, node, nodeAttributes, nodeNSChain, srcref):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def pushRaw(self, element):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def topInitialize(self):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def topAddData(self, data, srcref):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def topAddComment(self, comment):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def topFinalize(self):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def pop(self, node):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def popRaw(self):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~Reference Element Stack Implementation 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ElementStack(ElementStackAbstract):
    """This implementation is tied closely with ElementBase"""

    def buildElement(self, node, attributes, namespacemap):
        elemBuilder = self.getBuilder()
        args = (elemBuilder, self.topElementOrNone(), node, attributes, namespacemap)
        buildFactory = elemBuilder.getElementFactory(*args)
        element = buildFactory(*args)
        element.xmlBuildCreate(elemBuilder)
        return element

    def push(self, element, node, nodeAttributes, nodeNSChain, srcref):
        if self.stack:
            self.topElement().xmlAddElement(self.getBuilder(), node, element.xmlGetElement(self), srcref)
        self.pushRaw(element)
    def pushRaw(self, element):
        self.stack.append(element)

    def topInitialize(self):
        self.topElement().xmlInitStarted(self.getBuilder())
    def topPreAddElement(self, node, attributes, srcref):
        if self.stack:
            self.topElement().xmlPreAddElement(self.getBuilder(), node, attributes, srcref)
    def topAddData(self, data, srcref):
        self.topElement().xmlAddData(self.getBuilder(), data, srcref)
    def topAddComment(self, comment):
        self.topElement().xmlAddComment(self.getBuilder(), comment)
    def topFinalize(self):
        self.topElement().xmlInitFinalized(self.getBuilder())

    def pop(self):
        element = self.popRaw()
        element.xmlBuildComplete(self.getBuilder())
        result = element.xmlGetElement(self.getBuilder())
        if self.stack:
            self.topElement().xmlPostAddElement(self.getBuilder(), result)
        return result
    def popRaw(self):
        return self.stack.pop()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ElementBase(object):
    """Base class for objects created by ElementStack and related classes."""
    def __init__(self, elemBuilder, parentElem, node, attributes, namespaceMap):
        """This initialzer gets called only if the element class is used as it's factory"""
    def xmlBuildCreate(self, elemBuilder): 
        """Called just after creation of the element, but before the element is pushed onto the stack"""
    def xmlInitStarted(self, elemBuilder):
        """Called after the element is pushed onto the stack, but before subnodes are explored"""
    def xmlPreAddElement(self, elemBuilder, node, attributes, srcref):
        """Called whenever a subelement is encountered for this element, just after creation"""
    def xmlAddElement(self, elemBuilder, node, obj, srcref):
        """Called whenever a subelement is encountered for this element, just after creation"""
    def xmlPostAddElement(self, elemBuilder, obj):
        """Called whenever a subelement for this element has completed building"""
    def xmlAddData(self, elemBuilder, data, srcref):
        """Called whenever CDATA is encountered for this element"""
    def xmlAddComment(self, elemBuilder, comment):
        """Called whenever Comment data is encountered for this element"""
    def xmlInitFinalized(self, elemBuilder):
        """Called after all subnodes have been iterated, but before the element is popped off the stack"""
    def xmlBuildComplete(self, elemBuilder):
        """Called after the element is popped off the stack, before it goes out of 'scope'"""
    def xmlGetElement(self, elemBuilder):
        """Called whenever the "resultant" element is requested.  Allows for delegation"""
        return self

    #~ WeakRef Callbacks ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def asWeakRef(self): 
        return weakref.ref(self)
    def asWeakProxy(self): 
        return weakref.proxy(self)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ XMLBuilder
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class BuilderStatistics(object):
    markTime = staticmethod(systemTimer)

    def getResults(self, incHidden=False):
        results = vars(self).items()
        if not incHidden:
            results = [(name, value) for name, value in results if not name.startswith('_')]
        results.sort()
        return results

    def onBegin(self, skinner):
        self.__dict__.clear()

    def onEnd(self, skinner):
        pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Attributes(dict):
    def __init__(self, *args, **kw):
        dict.__init__(self, *args, **kw)

    def setMetaInfo(self, **kw):
        for n,v in kw.items():
            setattr(self, n, v)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class BuilderState(object):
    def __init__(self, xmlbuilder):
        self.elementStack = xmlbuilder.elementStack.saveState()
        self.namespaceChain = xmlbuilder.namespaceChain
        self._lastCompleteElement = xmlbuilder._lastCompleteElement
        self._parserCmd = xmlbuilder._parserCmd

    def restore(self, xmlbuilder):
        xmlbuilder.elementStack = self.elementStack
        xmlbuilder.namespaceChain = self.namespaceChain
        xmlbuilder._lastCompleteElement = self._lastCompleteElement
        xmlbuilder._parserCmd = self._parserCmd
        return True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class XMLBuilder(object): 
    """Guides the building of python objects from XML.  

    Depends upon the interface defined by ElementBase.

    See xmlNode or xmlClassBuilder for more concrete builders.
    """

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    seperator = ' '
    statistics = None

    xmlnsSynonyms = {}

    ElementFactory = ElementBase
    AttributeFactory = Attributes
    ElementStackFactory = ElementStack
    BuilderStateFactory = BuilderState
    StatisticsFactory = BuilderStatistics
    XMLParserFactory = ExpatParserCmd

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Protected Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _xmlnsGetSynonym(self, uri):
        # Don't forget to substitute our namespace synonyms!
        return self.xmlnsSynonyms.get(uri or None, uri) or None

    def _startNamespaceDeclHandler(self, prefix, uri):
        """Part of the tree-style template method, called at the before the beginning of an XML node parse 
        to manage namespaces."""
        # Add the prefix/uri to our current namespace mapping
        self.namespaceChain.setxmlns(prefix, self._xmlnsGetSynonym(uri))

    def _endNamespaceDeclHandler(self, prefix):
        """Part of the tree-style template method, called at the after the end of an XML node parse 
        to manage namespaces."""
        pass

    def _getAttributes(self, attributes):
        return self.AttributeFactory(attributes)

    def getElementFactory(self, elemBuilder, element, node, attributes, namespacemap):
        return self.ElementFactory

    def getElementStack(self):
        return self.elementStack

    def _startElement(self, name, attributes):
        srcref = self._getSourceFilenameAndLineNumber()
        return self._startElementEx(name, attributes, srcref)

    def _startElementEx(self, name, attributes, srcref):
        """Part of the tree-style template method, called at the beginning of an XML node parse.
        Instantiates the element returned by getElementFactory."""
        node = self._splitQualifiedName(name)
        nodeNSChain = self.namespaceChain

        nodeAttributes = self._getAttributes(attributes)
        nodeAttributes.setMetaInfo(node=node, srcref=srcref)

        self.elementStack.topPreAddElement(node, attributes, srcref)

        self.namespaceChain = self.namespaceChain.newChain()

        element = self.elementStack.buildElement(node, nodeAttributes, nodeNSChain)
        self.elementStack.push(element, node, nodeAttributes, nodeNSChain, srcref)
        self.elementStack.topInitialize()
        return element

    def _charData(self, data):
        """Part of the tree-style template method, called when CData is found."""
        srcref = self._getSourceFilenameAndLineNumber()
        self._charDataEx(data, srcref)

    def _charDataEx(self, data, srcref):
        return self.elementStack.topAddData(data, srcref)

    def _commentData(self, data):
        """Part of the tree-style template method, called when Comment data is found."""
        return self.elementStack.topAddComment(data)

    def _endElement(self, name):
        """Part of the tree-style template method, called at the closing of an XML node parse.
        Simply notifies the element that it is complete."""
        if self.elementStack:
            self.elementStack.topFinalize()
            self._lastCompleteElement = self.elementStack.pop()
            self.namespaceChain = self.namespaceChain.next().copy()
        else: 
            self.namespaceChain = None
            self._lastCompleteElement = None

        self.statistics.elements += 1
        return self._lastCompleteElement

    def _splitQualifiedName(self, combined):
        # rsplit
        idx = combined.rfind(self.seperator)
        if idx < 0: result = [None, combined]
        else: result = [combined[:idx], combined[idx+len(self.seperator):]]
        # end rsplit
        
        return self._xmlnsGetSynonym(result[0]), result[1]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ state save and restore - for advanced usage 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def saveState(self, *args, **kw):
        """Returns a state token that can be given to restoreState"""
        return self.BuilderStateFactory(self, *args, **kw)

    def restoreState(self, state, *args, **kw):
        """Uses the stack state token returned by saveState to restore the
        parsing stack to a prior level."""
        return state.restore(self, *args, **kw)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ parse template method
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def parse(self, xmlString, parseContext=None, **kw):
        """Starts the building of python objects using the XML parser.  Assumes
        first argument is string-like object."""
        return self.parseEx(xmlString, 'data', parseContext, **kw)

    def parseFile(self, xmlFile, parseContext=None, **kw):
        """Starts the building of python objects using the XML parser.  Assumes
        first argument is a file-like object."""
        return self.parseEx(xmlFile, 'file', parseContext, **kw)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getBuildResult(self):
        return self._lastCompleteElement

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Weakref Utils
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def asWeakRef(self):
        return weakref.ref(self)
    def asWeakProxy(self):
        return weakref.proxy(self)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Current Settings
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    _uri = None
    def getURI(self):
        parserCmd = self.getParserCmd()
        if parserCmd is not None:
            return parserCmd.getURI()
        else:
            return None
    uri = property(getURI)

    def _getSourceFilenameAndLineNumber(self):
        parserCmd = self.getParserCmd()
        if parserCmd is not None:
            return parserCmd.getSourceFilenameAndLineNumber()
        else: 
            return None

    _parserCmd = None
    def getParserCmd(self):
        return self._parserCmd
    def setParserCmd(self, parserCmd):
        previous = self._parserCmd
        self._parserCmd = parserCmd
        return previous
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Protected support 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _createParserCmd(self, xmlSource, parserInterface, parseContext):
        """Creates a callable object with interface specified by parserInterface using self.XMLParserFactory

        parserInterface:
            'data': returns a callable that takes a string of the XML document
            'file': returns a callable that takes a file-like interface to the XML document
            'raw': returns the raw parser object
        """
        return self.XMLParserFactory(self, xmlSource, parserInterface, parseContext)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def parseEx(self, xmlSource, parserInterface, parseContext, **kw):
        parserCmd = self._createParserCmd(xmlSource, parserInterface, parseContext)
        return self.parseCmd(parserCmd, **kw)

    def parseExRaw(self, xmlSource, parserInterface, parseContext, **kw):
        parserCmd = self._createParserCmd(xmlSource, parserInterface, parseContext)
        return self.parseCmdRaw(parserCmd, **kw)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def parseCmd(self, parserCmd, **kw):
        self._preParse()
        try:
            result = self.parseCmdRaw(parserCmd, **kw)
        except:
            # shutdown the parser, and reraise the execption
            self._abortParse()
            raise
        else:
            self._postParse()

        return result

    def parseCmdRaw(self, parserCmd, onBeforeParse=None, onAfterParse=None):
        previous = self.setParserCmd(parserCmd)
        try:
            if onBeforeParse:
                onBeforeParse(self, parserCmd)

            parserCmd()

            if onAfterParse:
                onAfterParse(self, parserCmd)
        finally:
            self.setParserCmd(previous)

        return self.getBuildResult()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _preParse(self):
        if hasattr(self, '_lastCompleteElement'):
            raise RuntimeError("An xml parse is already in progress from this instance!")

        self.elementStack = self.ElementStackFactory(self)
        self.namespaceChain = XMLNamespaceMap()
        self._lastCompleteElement = None

        if self.statistics is None:
            self.statistics = self.StatisticsFactory()
        self.statistics.onBegin(self)
        self.statistics.uri = self.getURI()
        self.statistics.elements = 0
        self.statistics._startTime = self.statistics.markTime()

    def _postParse(self):
        del self.elementStack
        del self.namespaceChain
        del self._lastCompleteElement

        ## Statistics related
        self.statistics._endTime = self.statistics.markTime()
        self.statistics.deltaTime = self.statistics._endTime - self.statistics._startTime
        self.statistics.elemPerSec = self.statistics.elements / max(1e-10, self.statistics.deltaTime)
        self.statistics.secPerElem = self.statistics.deltaTime / max(1, self.statistics.elements)
        self.statistics.onEnd(self)

    def _abortParse(self):
        if hasattr(self, '_lastCompleteElement'):
            del self._lastCompleteElement

