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

from TG.skinning.engine import XMLSkin
from TG.skinning.common.element import SkinElement
from template import template, store
import reference

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CompoundModelBase(object):
    def onSkinInitialize(self, element, elemBuilder):
        pass
    
    def onSkinFinalize(self, element, elemBuilder):
        pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Compound Model Mixins
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CompoundBaseElemMixin:
    CompoundModelFactory = CompoundModelBase
    def createCompoundModel(self, elemBuilder):
        compoundModel = self.CompoundModelFactory()
        if compoundModel is not None:
            self.setCompoundModel(compoundModel)
            compoundModel.onSkinInitialize(self, elemBuilder)

    def finalizeCompoundModel(self, elemBuilder):
        compoundModel = self.getCompoundModel()
        if compoundModel is not None:
            compoundModel.onSkinFinalize(self, elemBuilder)

    def getCompoundModel(self):
        raise NotImplementedError, "Subclass Responsibility"
    def setCompoundModel(self, model):
        raise NotImplementedError, "Subclass Responsibility"
    def delCompoundModel(self):
        raise NotImplementedError, "Subclass Responsibility"

class UnifiedCompoundElemMixin(CompoundBaseElemMixin):
    def getCompoundModel(self):
        return self.getObject()
    def setCompoundModel(self, model):
        self.setObject(model)
    def delCompoundModel(self):
        self.delObject()

class SeparateCompoundElemMixin(CompoundBaseElemMixin):
    _compoundModel = None
    def getCompoundModel(self):
        return self._compoundModel
    def setCompoundModel(self, model):
        self._compoundModel = model
    def delCompoundModel(self):
        del self._compoundModel

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
class CompoundElement(store.ElementRestoreMixin, SkinElement):
    """This object is meant to be derived from in order to generate compound skin elements.
    
    In the derived class, place the compound object's xml skin description in
    xmlSkin, then instantiate as usual."""

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    _ctxHostObjNames = ('host', )
    _ctxHostElemNames = ('hostElem', )

    defaultSettings = SkinElement.defaultSettings.copy()
    defaultSettings.update({
        'ctx-push':'True',
        'unravel-stop': '1',
        })

    invokeName = "::contents"

    xmlSkin = """<?xml version='1.0'?><template expand='::contents'/>"""

    xmlFactories = template.xmlFactories

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def initSkinContext(self, elemBuilder, xmlParent):
        SkinElement.initSkinContext(self, elemBuilder, xmlParent)

    def xmlInitStarted(self, elemBuilder):
        self.createCompoundModel(elemBuilder)
        self.saveSettingsInContext()
        self.pushContext() # This needs to happen before self.initSkinSettings
        elemBuilder.pushXMLFactories(self.xmlFactories)
        return SkinElement.xmlInitStarted(self, elemBuilder)

    def xmlInitFinalized(self, elemBuilder):
        SkinElement.xmlInitFinalized(self, elemBuilder)
        elemBuilder.popXMLFactories()

        self.setStoringState(False)
        invokeName = '::invoke:'+self.invokeName
        self.setContextVar(invokeName, self.asWeakProxy())
        self.referenceCompoundSkin(elemBuilder)
        self.delContextVar(invokeName)
        self.delStoredChildren()
        
        self.finalizeCompoundModel(elemBuilder)

        self.removeSettingsInContext()
        
    def getCompoundModel(self):
        raise NotImplementedError, "Subclass Responsibility"
    def setCompoundModel(self, model):
        raise NotImplementedError, "Subclass Responsibility"
    def delCompoundModel(self):
        raise NotImplementedError, "Subclass Responsibility"

    def getCompoundSkin(self):
        return self.xmlSkin
    def referenceCompoundSkin(self, elemBuilder):
        return self.referenceSkin(elemBuilder, self.getCompoundSkin())

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    referenceSkin = reference.referenceSkin
    referenceSkinFile = reference.referenceSkinFile
    referenceSkinParseContext = reference.referenceSkinParseContext

    Unified = UnifiedCompoundElemMixin
    Separate = SeparateCompoundElemMixin

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class UnifiedCompoundElement(CompoundElement.Unified, CompoundElement):
    pass
class SeparateCompoundElement(CompoundElement.Separate, CompoundElement):
    pass

