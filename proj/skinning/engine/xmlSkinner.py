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

from TG.w3c import xmlBuilder
from TG.w3c.xmlClassBuilder import XMLClassBuilder, XMLFactory
from TG.w3c.xmlBuilderWithCSS import XMLBuilderCSSMixin

from TG.skinning.common import css as cssSkinning
from TG.skinning.common import cssElement
from TG.skinning.common import element

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def _installSkins(host, *skins, **kw):
    for skin in skins:
        if callable(skin): skin(host, **kw)
        else: skin.install(host, **kw)
    return host

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class PrintBuilderStatistics(xmlBuilder.BuilderStatistics):
    def onEnd(self, skinner):
        print "End skinning.  Stats:"
        for name, value in self.getResults():
            if isinstance(value, float):
                value = '%.3f' % (value)
            print "    %-10s : %s" % (name, value)
        print

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class XMLSkinnerBase(XMLClassBuilder):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    ContextFactory = element.SkinContext
    xmlnsSynonyms = {}
    xmlFactories = XMLFactory.Collection()
    xmlFactories.setName('root')
    _context = None

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getURIResolver(self):
        return self.getURI()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def installSkins(self, *skins, **kw):
        self._assureLocalFactories()
        return _installSkins(self, *skins, **kw)
    installClassSkins = classmethod(_installSkins)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def skin(self, xmlString, parseContext=None, **kw):
        return self._skinEx(xmlString, 'data', parseContext, **kw)
    def skinFile(self, xmlFile, parseContext=None, **kw):
        return self._skinEx(xmlFile, 'file', parseContext, **kw)

    def skinFromStack(self, xmlString, parseContext=None, **kw):
        return self._skinFromStackEx(xmlString, 'data', xmlString, parseContext, **kw)
    def skinFileFromStack(self, xmlFile, parseContext=None, **kw):
        return self._skinFromStackEx(xmlFile, 'file', parseContext, **kw)

    def graftSkin(self, xmlString, parentElemOrList, parseContext=None, *args, **kw):
        return self._graftSkinEx(xmlString, 'data', parentElemOrList, parseContext=None, *args, **kw)
    def graftSkinFile(self, xmlFile, parentElemOrList, parseContext=None, *args, **kw):
        return self._graftSkinEx(xmlFile, 'file', parentElemOrList, parseContext=None, *args, **kw)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Context Related 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def pushContextKw(self, kw=None, srcctx=None):
        if srcctx is None:
            srcctx = self.getContext()
        if kw:
            ctx = self.ContextFactory.fromKeywords(srcctx , **kw)
        else: 
            ctx = self.ContextFactory(srcctx)
        return self.pushContext(ctx)

    def pushContext(self, ctx):
        return self.setContext(ctx)
    def popContext(self, ctx):
        return self.setContext(ctx)

    def getContext(self, create=False):
        if create and self._context is None:
            self.pushContextKw()
        return self._context
    def setContext(self, context):
        previous = self._context
        self._context = context
        return previous
    ctx = context = property(getContext) # assignment shouldn't be too convienient

    def addContextKw(self, **kw):
        ctx = self.getContext(True)
        for n,v in kw.items():
            setattr(ctx, n, v)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Protected Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _preSkin(self, _srcctx=None, **kw):
        return self.pushContextKw(kw, _srcctx)

    def _postSkin(self, prevCtx):
        self.popContext(prevCtx)

    def _assureLocalFactories(self):
        if 'xmlFactories' not in self.__dict__:
            self.xmlFactories = self.xmlFactories.copy()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _skinEx(self, data, isFile, parseContext=None, **kw):
        token = self._preSkin(**kw)
        try: 
            result = self.parseEx(data, isFile, parseContext)
        finally: 
            self._postSkin(token)
        return result

    def _skinFromStackEx(self, data, isFile, parseContext=None, **kw):
        topElement = self.elementStack.topElement()
        token = self._preSkin(topElement.getContext(), **kw)
        topElement.pushContext(force=True, ctx=self.getContext())

        try: 
            xmlnsSynonyms = self.xmlnsSynonyms 
            self.xmlnsSynonyms = self.xmlnsSynonyms.copy()
            self.xmlnsSynonyms[None] = self.namespaceChain.xmlns('')

            result = self.parseExRaw(data, isFile, parseContext)
        finally: 
            self.xmlnsSynonyms = xmlnsSynonyms
            self._postSkin(token)
            topElement.popContext(force=True)

        return result
  
    def _graftSkinEx(self, data, isFile, parentElemOrList, parseContext=None, *args, **kw):
        if not isinstance(parentElemOrList, list):
            parentElemOrList = [parentElemOrList]
        parentElem = parentElemOrList[-1]

        #~ ~ ~ ~ ~ ~ ~ ~ ~
        def onBeforeParse(self, parserCmd):
            for elem in parentElemOrList:
                self.elementStack.pushRaw(elem)
        def onAfterParse(self, parserCmd):
            for elem in parentElemOrList[::-1]:
                result = self.elementStack.popRaw()
                if result is not elem:
                    raise RuntimeError("Inconsistent skin stack result")
        #~ ~ ~ ~ ~ ~ ~ ~ ~

        token = self._preSkin(parentElem.getContext(), **kw)
        parentElem.pushContext(force=True, ctx=self.getContext())
        try: 
            result = self.parseEx(data, isFile, parseContext,
                        onBeforeParse=onBeforeParse, onAfterParse=onAfterParse)
        finally: 
            self._postSkin(token)
            parentElem.popContext(force=True)
        return result

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ XMLSkinner with CSS mixed in :)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class XMLSkinnerWithCSS(XMLBuilderCSSMixin, XMLSkinnerBase):
    CSSParserFactory = cssSkinning.CSSParser
    ContextFactory = cssElement.CSSSkinContext

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Alaises
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

XMLSkinner = XMLSkinnerWithCSS

