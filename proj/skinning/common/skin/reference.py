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

import os
from TG.introspection.stack import traceSrcrefEval
from TG.skinning.engine.parseContext import URISkinParseContext, XMLSkinParseContext
from TG.skinning.common.cssElement import CSSSkinElement

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# We share these methods outside of the class for increased reuse

def referenceSkinParseContext(self, elemBuilder, parseContext, *args, **kw):
    resourceFile = parseContext.openFile() 
    try:
        result = traceSrcrefEval(self._settings.srcref, 'reference()',
                    reference=lambda: elemBuilder.skinFileFromStack(resourceFile, parseContext, *args, **kw))
    finally:
        resourceFile.close()
    return result
    
def referenceSkinFile(self, elemBuilder, resourceName, *args, **kw):
    uriSource = self.getURIResolver().resolve(resourceName)
    parseContext = URISkinParseContext(uriSource)

    return self.referenceSkinParseContext(elemBuilder, parseContext, *args, **kw)

def referenceSkin(self, elemBuilder, xmlString, *args, **kw):
    if isinstance(xmlString, basestring):
        parseContext = XMLSkinParseContext.fromSourceData(xmlString, self.getURIResolver())
    else:
        parseContext = xmlString
        if parseContext.getURINode() is None:
            parseContext.setURINode(self.getURIResolver())
    return self.referenceSkinParseContext(elemBuilder, parseContext, *args, **kw)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class reference(CSSSkinElement):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    defaultSettings = CSSSkinElement.defaultSettings.copy()
    defaultSettings.update({
        'ctx-push':'True',
        })

    defaultStyleSettings = CSSSkinElement.defaultStyleSettings.copy()
    defaultStyleSettings.update({
        'ref': '',
        'fromctx': '',
        })

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Definitions 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def xmlInitStarted(self, elemBuilder):
        self.setSetting('unravel', 'down')
        return CSSSkinElement.xmlInitStarted(self, elemBuilder)

    def xmlBuildComplete(self, elemBuilder):
        ref = self.getStyleSettingRef()
        if ref:
            self.referenceSkinFile(elemBuilder, ref)
        elif self.referenceUsingFromCtx(elemBuilder):
            pass
        else:
            raise RuntimeError("<reference/> must specify either ref or fromctx attribute")
        CSSSkinElement.xmlBuildComplete(self, elemBuilder)

    def referenceUsingFromCtx(self, elemBuilder):
        fromctx = self.getStyleSettingInContext('fromctx', None)
        if callable(fromctx):
            # Delegate responsibility to callable method
            fromctx(self, elemBuilder)
            return True
        elif fromctx:
            self.referenceSkin(elemBuilder, fromctx)
            return True
        return False

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    _raw_referenceSkin = referenceSkin
    def referenceSkin(self, elemBuilder, xmlString, *args, **kw):
        elem = self._raw_referenceSkin(elemBuilder, xmlString, *args, **kw)
        return self._setPassthrough(elem)

    _raw_referenceSkinFile = referenceSkinFile
    def referenceSkinFile(self, elemBuilder, resourceName, *args, **kw):
        elem = self._raw_referenceSkinFile(elemBuilder, resourceName, *args, **kw)
        return self._setPassthrough(elem)

    referenceSkinParseContext = referenceSkinParseContext

    def _setPassthrough(self, elem):
        self.setElement(elem)
        try:
            getObj = elem.getObject
        except AttributeError:
            obj = None
        else:
            obj = getObj()
        self.setObject(obj)
        return obj

