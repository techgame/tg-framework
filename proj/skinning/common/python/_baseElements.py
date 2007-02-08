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

import types

from TG.introspection.code import compileWithFileAndLine
from TG.skinning.common.element import SkinElement
from TG.skinning.common.skin.ignore import IgnoreXML
from TG.w3c.xmlClassBuilder import XMLFactory

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SkinXMLModule(types.ModuleType):
    pass

class PythonSkinElement(SkinElement):
    SkinModuleFactory = SkinXMLModule
    defaultSettings = SkinElement.defaultSettings.copy()
    defaultSettings.update({'unravel': 'down'})
    elementGlobals = {}
    elementLocals = {}
    elementModule = None

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def xmlInitStarted(self, elemBuilder):
        self._initChunks(elemBuilder)
        return SkinElement.xmlInitStarted(self, elemBuilder)

    def xmlAddData(self, elemBuilder, data, srcref):
        SkinElement.xmlAddData(self, elemBuilder, data, srcref)
        self.content.append(data)
        self.srcrefContent = srcref

    def xmlPreAddElement(self, elemBuilder, name, attributes, srcref):
        self._chunkContent(elemBuilder)
        return SkinElement.xmlPreAddElement(self, elemBuilder, name, attributes, srcref)
    def xmlPostAddElement(self, elemBuilder, elem):
        self._chunkContent(elemBuilder)
        return SkinElement.xmlPostAddElement(self, elemBuilder, elem)

    def xmlInitFinalized(self, elemBuilder):
        SkinElement.xmlInitFinalized(self, elemBuilder)
        self._chunkContent(elemBuilder, last=True)

    def xmlBuildComplete(self, elemBuilder):
        self._cleanupChunks(elemBuilder)
        SkinElement.xmlBuildComplete(self, elemBuilder)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _initChunks(self, elemBuilder):
        self.content = []
        self.contentChunks = []
        self.srcrefContent = self._settings.srcref

    def _chunkContent(self, elemBuilder, last=False):
        content = ''.join(self.content)
        self.content[:] = []

        fn, line = self.srcrefContent
        self.srcrefContent = fn, line - content.count('\n')
        if content.strip():
            self._executeContent(elemBuilder, content)
        elif last:
            self._executeContent(elemBuilder, None)

    def _cleanupChunks(self, elemBuilder):
        del self.content
        del self.contentChunks
        del self.srcrefContent
        self.delGlobals()
        self.delLocals()

    def _executeContent(self, elemBuilder, content):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

    #~ Python Execution Helpers ~~~~~~~~~~~~~~~~~~~~~~~~~

    def compile(self, source, mode='exec', codeTemplate='', lineOffset=0, ):
        global compileWithFileAndLine

        # manage the line numbers
        if mode == 'exec': # exec's happen only in the content area
            srcName, lineNumber = self.srcrefContent
            lineNumber -= lineOffset
        else:
            # use the element line as the starting line number when we don't know.
            # Although this won't be strictly correct, at least it will get
            # them to general area of the problem causing item.  Then they can
            # look for CSS rules, etc.
            srcName, lineNumber = self._settings.srcref
            lineNumber -= lineOffset

        if codeTemplate:
            source = codeTemplate % source

        code = compileWithFileAndLine(source, mode, srcName, lineNumber)
        return code

    def evaluate(self, code, codeTemplate='%s', **kw):
        if isinstance(code, basestring):
            code = self.compile(code, 'eval', codeTemplate)
        return eval(code, self.getGlobals() or {}, self.getLocals(**kw) or {})

    def execute(self, code, codeTemplate='%s', **kw):
        if isinstance(code, basestring):
            code = self.compile(code, 'exec', codeTemplate)
        exec code in self.getExecVars(**kw)

    def getExecModule(self):
        if self.elementModule is None:
            self.elementModule = self.SkinModuleFactory('dynamic:'+self.__class__.__name__)
            self.elementModule.__dict__.update(self.getExecGlobals())
        return self.elementModule
    module = property(getExecModule)

    def getExecVars(self, **kw):
        module = self.getExecModule()
        module.__dict__.update(self.getExecLocals())
        module.__dict__.update(kw)
        return module.__dict__

    def getGlobals(self):
        return self.elementGlobals
    getExecGlobals = getGlobals
    def setGlobals(self, elementGlobals):
        self.elementGlobals = elementGlobals
    def delGlobals(self):
        if 'elementGlobals' in self.__dict__:
            del self.elementGlobals

    def getLocals(self, **kw):
        if 'elementLocals' not in self.__dict__:
            self.setLocals(self.createLocals())
        self.refreshLocals(self.elementLocals)
        if kw:
            kw.update(self.elementLocals)
            return kw
        else: return self.elementLocals
    getExecLocals = getLocals
    def setLocals(self, elementLocals):
        self.elementLocals = elementLocals
    def delLocals(self):
        if 'elementLocals' in self.__dict__:
            del self.elementLocals
    def createLocals(self):
        return self.elementLocals.copy()
    def refreshLocals(self, elementLocals):
        elementLocals.update({
            'pyelem':self, 
            'elem':self,
            'ctx':self.getContext(),
            'obj':self.getObject(),
            })

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class PassThroughElement(PythonSkinElement):
    passThruState = True

    def xmlPreAddElement(self, elemBuilder, name, attributes, srcref):
        if self.passThruState and self.xmlParent():
            self._chunkContent(elemBuilder)
            return self.xmlParent().xmlPreAddElement(elemBuilder, name, attributes, srcref)
        else:
            return PythonSkinElement.xmlPreAddElement(self, elemBuilder, name, attributes, srcref)
    def xmlAddElement(self, elemBuilder, node, elem, srcref):
        if self.passThruState and self.xmlParent():
            return self.xmlParent().xmlAddElement(elemBuilder, node, elem, srcref)
        else:
            return PythonSkinElement.xmlAddElement(self, elemBuilder, node, elem, srcref)
    def xmlPostAddElement(self, elemBuilder, elem):
        if self.passThruState and self.xmlParent():
            return self.xmlParent().xmlPostAddElement(elemBuilder, elem)
        else:
            return PythonSkinElement.xmlPostAddElement(self, elemBuilder, elem)

    def refreshLocals(self, elementLocals):
        xmlParent = self.xmlParent()
        if xmlParent is not None: 
            obj = xmlParent.getObject()
        else: obj = None

        elementLocals.update({
            'pyelem':self, 
            'elem':xmlParent, 
            'ctx':self.getContext(),
            'obj':obj,
            })

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ConditionalElement(PassThroughElement):
    ignoreFactories = XMLFactory.Collection({
            None: XMLFactory.Static(IgnoreXML),
        }).setName('ConditionalElement')

    def xmlInitFinalized(self, elemBuilder):
        self.setNormalState(elemBuilder)
        PassThroughElement.xmlInitFinalized(self, elemBuilder)

    def setIgnoreState(self, elemBuilder):
        if self.passThruState:
            self.passThruState = False
            elemBuilder.pushXMLFactories(self.ignoreFactories)

    def setNormalState(self, elemBuilder):
        if not self.passThruState:
            self.passThruState = True
            factories = elemBuilder.popXMLFactories()
            assert factories is self.ignoreFactories

