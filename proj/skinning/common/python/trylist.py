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

from TG.w3c.xmlBuilder import ElementFactoryError
from TG.skinning.engine.xmlSkinner import XMLFactory
from TG.skinning.common.skin.store import StoreXML, RestoreMixin
from _baseElements import PythonSkinElement

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Class
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class trylist(RestoreMixin, PythonSkinElement):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    defaultSettings = PythonSkinElement.defaultSettings.copy()
    defaultSettings.update({
        'unravel': 'down',
        'catch': '(ImportError, ElementFactoryError)',
        'when': 'outside',
        })

    elementLocals = PythonSkinElement.elementLocals.copy()
    elementLocals.update({
        'ElementFactoryError': ElementFactoryError, 
        'EFE': ElementFactoryError,
        })

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def xmlInitStarted(self, elemBuilder):
        elemBuilder.pushXMLFactories(self.xmlFactories)
        return PythonSkinElement.xmlInitStarted(self, elemBuilder)

    def xmlInitFinalized(self, elemBuilder):
        if self.getSetting('when') == 'inside':
            elemBuilder.popXMLFactories()
            self.tryRestoreElemenets(elemBuilder)
        PythonSkinElement.xmlInitFinalized(self, elemBuilder)

    def xmlBuildComplete(self, elemBuilder):
        if self.getSetting('when') == 'outside':
            elemBuilder.popXMLFactories()
            self.tryRestoreElemenets(elemBuilder)
        PythonSkinElement.xmlBuildComplete(self, elemBuilder)

    def _chunkContent(self, elemBuilder, last=False):
        pass

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def tryRestoreElemenets(self, elemBuilder):
        self.setStoringState(False)
        catch = self.getSetting('catch')
        catchTypes = self.evaluate(catch)

        self.setObject(None)
        stackstate = elemBuilder.saveState()
        for isnode, child, srcref in self.getStoredChildren():
            if not isnode: continue

            try:
                result = child.restore(elemBuilder)
                if result is not None:
                    break
            except catchTypes, e:
                # Adjust the element stack to what it was when wes started
                elemBuilder.restoreState(stackstate)
                self.setObject(e)

from __init__ import namespace
trylist._createXMLFactories(namespace)

