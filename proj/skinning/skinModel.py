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

import warnings
import weakref

from TG.skinning.engine import xmlSkinner
from TG.skinning.engine import XMLSkin, XMLSkinParseContext, URISkinParseContext
from TG.skinning import resolvers

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SkinModel(object):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    xmlSkin = None
    xmlSkinRef = None
    xmlSkinHref = None

    xmlSkinnerFactory = xmlSkinner.XMLSkinnerWithCSS
    xmlStatisticsFactory = xmlSkinner.PrintBuilderStatistics
    xmlSkinnerInstalls = []

    ctxobj = 'model'
    _skinRoot = None
    _uriNode = None
    _uriResolvers = []

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __init__(self, filepath=None):
        if filepath is None:
            if self.xmlSkinRef:
                self.filepath = self.xmlSkinRef
            elif self.xmlSkinHref:
                warnings.warn('Use of xmlSkinHref attribute is depreciated.  Please use xmlSkinRef instead.', DeprecationWarning)
                self.filepath = self.xmlSkinHref
            else:
                filepath = '.'
        self.setURINodePath(filepath)

    def fromSkinRef(klass, xmlSkinRef, *args, **kw):
        self = klass(*args, **kw)
        self.xmlSkinRef = xmlSkinRef
        return self
    fromSkinRef = classmethod(fromSkinRef)
    def fromSkinHref(klass, xmlSkinHref, *args, **kw):
        warnings.warn('Use of fromSkinHref is depreciated.  Please use fromSkinRef instead.', DeprecationWarning)
        return klass.fromSkinRef(xmlSkinHref, *args, **kw)
    fromSkinHref = classmethod(fromSkinHref)

    def fromSkin(klass, xmlSkin, *args, **kw):
        self = klass(*args, **kw)
        self.xmlSkin = xmlSkin
        return self
    fromSkin = classmethod(fromSkin)

    #~ skinModel methods ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def skinModel(self, **ctxvars):
        parseContext = self._getParseContextForModel()
        return self._skinFromParseContext(parseContext, self._getXMLSkinner(), **ctxvars)

    def skinModelFromCtx(self, ctx, **ctxvars):
        parseContext = self._getParseContextForModel()
        return self._skinFromParseContext(parseContext, ctx.skinner, **ctxvars)

    def skinModelFromReference(self, reference, elemBuilder, **ctxvars):
        parseContext = self._getParseContextForModel()
        return self._skinFromParseContext(parseContext, elemBuilder, fromStack=True, **ctxvars)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def skinRef(self, ref, **ctxvars):
        parseContext = self._getParseContextFromRef(ref)
        return self._skinFromParseContext(parseContext, self._getXMLSkinner(), **ctxvars)

    def skinRefFromCtx(self, ref, ctx=None, **ctxvars):
        if ctx is None: ctx = self.ctx
        parseContext = self._getParseContextFromRef(ref)
        return self._skinFromParseContext(parseContext, ctx.skinner, **ctxvars)

    def skinXML(self, xml, **ctxvars):
        parseContext = self._getParseContextFromXML(xml)
        return self._skinFromParseContext(parseContext, self._getXMLSkinner(), **ctxvars)

    def skinXMLFromCtx(self, xml, ctx=None, **ctxvars):
        if ctx is None: ctx = self.ctx
        parseContext = self._getParseContextFromXML(xml)
        return self._skinFromParseContext(parseContext, ctx.skinner, **ctxvars)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _skinFromParseContext(self, parseContext, skinner, fromStack=False, **ctxvars):
        if parseContext.getURINode() is None:
            parseContext.setURINode(self.getURINode())

        xmlSkinFile = parseContext.openFile()
        try:
            # get context vars
            ctxvars = self._getSkinModelContext(skinner, **ctxvars)

            # Skin it!
            self.onSkinModelStarted(skinner)
            if fromStack:
                skinRoot = skinner.skinFileFromStack(xmlSkinFile, parseContext, **ctxvars)
            else:
                skinRoot = skinner.skinFile(xmlSkinFile, parseContext, **ctxvars)
            self.setSkinRoot(skinRoot)
            self.onSkinModelComplete(skinner, skinRoot)
        finally:
            xmlSkinFile.close()

        return skinRoot

    #~ onSkinModel overrides ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def onSkinModelStarted(self, skinner):
        pass

    def onSkinModelComplete(self, skinner, skinnedRoot):
        pass

    #~ Properties after model is skinned ~~~~~~~~~~~~~~~~

    def getSkinRoot(self):
        return self._skinRoot
    def setSkinRoot(self, skinRoot):
        self._skinRoot = skinRoot
    def delSkinRoot(self):
        del self._skinRoot
    skinRoot = property(getSkinRoot, setSkinRoot, delSkinRoot)

    def getSkinContext(self):
        skinRoot = self.getSkinRoot()
        if skinRoot is not None:
            return skinRoot.ctx
        else: 
            return None
    ctx = context = property(getSkinContext)

    #~ WeakRef Callbacks ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def asWeakRef(self):
        return weakref.ref(self)

    def asWeakProxy(self):
        return weakref.proxy(self)

    #~ Protected methods for overriding ~~~~~~~~~~~~~~~~~

    def _getSkinModelContext(self, skinner, **ctxvars):
        ctxvars[self.ctxobj] = self.asWeakProxy()
        return ctxvars

    def _getParseContextFromRef(self, ref):
        uriNode = self.getURIResolver().resolve(ref)
        parseContext = URISkinParseContext(uriNode)
        return parseContext

    def _getParseContextFromXML(self, xmlSkin):
        if isinstance(xmlSkin, basestring):
            parseContext = XMLSkinParseContext.fromSourceData(xmlSkin, self.getURINode())
        else:
            parseContext = xmlSkin
        return parseContext

    def _getParseContextForModel(self):
        if self.xmlSkinRef is not None:
            return self._getParseContextFromRef(self.xmlSkinRef)
        elif self.xmlSkinHref is not None:
            warnings.warn('Use of xmlSkinHref is depreciated.  Please use xmlSkinRef instead.', DeprecationWarning)
            return self._getParseContextFromRef(self.xmlSkinHref)
        elif self.xmlSkin is not None:
            return self._getParseContextFromXML(self.xmlSkin)
        else:
            raise RuntimeError("%r does not have an valid 'xmlSkin' or 'xmlSkinRef'." % (self,))

    #~ XMLSkinner acquisition and creation ~~~~~~~~~~~~~

    def _getXMLSkinner(self):
        skinner = self.xmlSkinnerFactory()
        self._xmlSkinnerInitialize(skinner)
        return skinner

    def _xmlSkinnerInitialize(self, skinner):
        if self.xmlSkinnerInstalls:
            skinner.installSkins(*self.xmlSkinnerInstalls)

        self._xmlSkinnerStatistics(skinner)

    def _xmlSkinnerStatistics(self, skinner):
        if self.xmlStatisticsFactory is not None:
            skinner.StatisticsFactory = self.xmlStatisticsFactory

    #~ URI Resolver acquisition ~~~~~~~~~~~~~~~~~~~~~~~

    def getURINode(self):
        return self._uriNode
    def setURINode(self, uriNode):
        self._uriNode = uriNode
    uriNode = property(getURINode, setURINode)

    def getURI(self, resolvable=False):
        if resolvable:
            return self.getURINode().asResolvableURI()
        else:
            return self.getURINode().getURI()

    def setURINodePath(self, filepath):
        fnResolver = self._getResolversRegistry('filename')
        uriNode = fnResolver.resolve(filepath, mustExist=False)
        self.setURINode(uriNode)

    def getURIResolver(self):
        resolver = self.getURINode()
        if resolver is None:
            resolver = self._getResolversRegistry('skin')
        return resolver 

    def setURIResolver(self, uriResolver):
        previous = self.getURINode()
        self.setURINode(uriResolver)
        return previous

    def _getResolversRegistry(self, key=NotImplemented):
        if key is NotImplemented:
            return resolvers.registry
        else:
            return resolvers.registry[key]

