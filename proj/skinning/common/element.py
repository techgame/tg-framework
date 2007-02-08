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

from TG.common.utilities import strToList as _strToList, boolFromStr as _boolFromStr

from TG.common.scopes import LinkedScope as _SkinContextBase
from TG.w3c.xmlBuilder import ElementBase as _SkinElementBase

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Skin Context
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SkinContext(_SkinContextBase):
    def fromKeywords(klass, *args, **kw):
        result = klass(*args)
        for n,v in kw.items():
            setattr(result, n, v)
        return result
    fromKeywords = classmethod(fromKeywords)

    def getSelf(self):
        return self
    ctx = property(getSelf)

    def getRootContext(self):
        return self.rootScope()
    root = property(_SkinContextBase.rootScope)

    def getAddressedName(self, addrStr, sliceEnd=None):
        """Like getattr, but can deal with dotted names"""
        result = self
        addr = addrStr.split('.')
        for each in addr[:sliceEnd]:
            result = getattr(result, each)
        if sliceEnd: 
            return result, addr[-1]
        else: 
            return result

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getSkinner(self):
        return self.skinner
    def setSkinner(self, skinner):
        self.skinner = skinner
        self.setURI(skinner.getURI())

    def onNewSkinElement(self, skinElement):
        """Called when a new skin is created, signifying a scope for CSS or other scope dependent things"""
        pass

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getURI(self):
        return self._uri
    def setURI(self, uri):
        self._uri = uri
    uri = property(getURI, setURI)

    def getURIResolver(self):
        uri = self.getURI()
        if not isinstance(uri, basestring):
            return uri

    def add(self, nameOrValue, value=NotImplemented):
        if value is NotImplemented:
            value = nameOrValue
            nameOrValue = value.__name__
        setattr(self, nameOrValue, value)
        return value

#~ Build Temp for transitory values while building ~

class SkinBuildTemp(object):
    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.__dict__)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Skin Element
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SkinElement(_SkinElementBase):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    defaultSettings = {}
    BuildTempFactory = SkinBuildTemp
    SkinContextFactory = SkinContext

    _obj = None
    _ctx = None
    _children = None
    _ctxPushed = 0
    _ctxHostObjNames = ()
    _ctxHostElemNames = ()
    _xmlParent = None

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ xmlBuilder.ElementBase Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __init__(self, *args, **kw):
        """This initialzer gets called only if the element class is used as it's factory"""
        self.initElement(*args, **kw)

    def xmlBuildCreate(self, elemBuilder): 
        """Called just after creation of the element, but before the element is pushed onto the stack"""
        self._xmlBuildTemp = self.BuildTempFactory()
        self._xmlBuildTemp.elemBuilder = elemBuilder

    def xmlInitStarted(self, elemBuilder):
        """Called after the element is pushed onto the stack, but before subnodes are explored"""
        self.setInitialContext()

    def xmlPreAddElement(self, elemBuilder, name, attributes, srcref):
        """Called whenever a subelement is encountered for this element, just after creation"""
    def xmlAddElement(self, elemBuilder, node, element, srcref):
        """Called whenever a subelement is encountered for this element, just after creation"""
        self.addElement(element, srcref)
    def xmlPostAddElement(self, elemBuilder, element):
        """Called whenever a subelement for this element has completed building"""
    def xmlAddData(self, elemBuilder, data, srcref):
        """Called whenever CDATA is encountered for this element"""

    def xmlInitFinalized(self, elemBuilder):
        """Called after all subnodes have been iterated, but before the element is popped off the stack"""

    def xmlBuildComplete(self, elemBuilder):
        """Called after the element is popped off the stack, before it goes out of 'scope'"""
        try:
            self.setFinalContext()
            self.checkUnravel(elemBuilder)
        finally:
            if hasattr(self, '_xmlBuildTemp'):
                del self._xmlBuildTemp

    def xmlGetElement(self, elemBuilder):
        """Called whenever the "resultant" element is requested.  Allows for delegation"""
        return self

    def getXMLParent(self):
        if self._xmlParent is not None:
            return self._xmlParent()
    xmlParent = getXMLParent
    def setXMLParent(self, xmlParent):
        if xmlParent is not None:
            self._xmlParent = xmlParent.asWeakRef()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ SkinElement methods
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def initElement(self, elemBuilder, parentElem, node, attributes, namespaceMap):
        self.initSkinParent(elemBuilder, parentElem)
        self.initSkinContext(elemBuilder, parentElem)
        self.initSkinSettings(elemBuilder, node, attributes, namespaceMap)

    def initSkinParent(self, elemBuilder, xmlParent):
        if xmlParent is not None: 
            self.setXMLParent(xmlParent)

    def initSkinContext(self, elemBuilder, xmlParent):
        ctx = getattr(xmlParent, 'ctx', None)
        while (ctx is None) and (xmlParent is not None):
            xmlParent = xmlParent.xmlParent()
            ctx = getattr(xmlParent, 'ctx', None)

        if ctx is None:
            ctx = elemBuilder.getContext()
            if ctx is None:
                ctx = self.pushContext()
            ctx.setSkinner(elemBuilder)

        self.setContext(ctx)

    #~ SkinElement Settings ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def filterSettings(self, attributes):
        key = attributes.pop('T-settings-', None)
        if key is not None:
            settings = getattr(self.getContext(), key, None)
            attributes.update(settings)

        return attributes

    def initSkinSettings(self, elemBuilder, node, attributes, namespaceMap):
        self._settings = self.filterSettings(attributes)
        self.setupCSSElement(elemBuilder, node, attributes, namespaceMap)

    def hasSetting(self, name, includeDefault=False):
        if name in self._settings:
            return True
        elif includeDefault and (name in self.defaultSettings):
            return True
        else: 
            return False
    def getSetting(self, name, default=NotImplemented, weakDefault=NotImplemented):
        if name in self._settings:
            return self._settings[name]
        elif default is not NotImplemented:
            return default
        elif name in self.defaultSettings:
            return self.defaultSettings[name]
        elif weakDefault is not NotImplemented:
            return weakDefault
        raise LookupError("Could not find a setting for \'%s\'" % (name,))
    def setSetting(self, name, value):
        self._settings[name] = value

    def getSettingRef(self, default=''):
        return self.getSetting('ref', None) or self.getSetting('href', default)

    def getSettingInContext(self, name, default=NotImplemented):
        value = self.getSetting(name, None)
        return self._getSettingInContextImpl(value, name, default)

    def _getSettingInContextImpl(self, value, name, default=NotImplemented):
        if value is not None:
            ctx = self.getContext()
            try: 
                return ctx.getAddressedName(value)
            except AttributeError: 
                pass

        if default is NotImplemented:
            raise LookupError('Could not find setting "%s" in context' % (value,))
        else: 
            return default

    def getSettingAsAddress(self, name, default=NotImplemented, ctx=None, useParentContext=False):
        addr = self.getSetting(name, default)
        if ctx is None:
            if ('.' in addr) or not useParentContext:
                ctx = self.getContext()
            else:
                ctx = self.getParentContext()
        if addr is not None:
            result = ctx.getAddressedName(addr, -1)
            return result
        else: 
            return ctx

    #~ CSS related ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def isCSSEnabled(self): return False
    def getCSSElement(self): return None
    def setupCSSElement(self, elemBuilder, node, attributes, namespaceMap): pass
    def addCSSElement(self, element, srcref): pass
    def getCSSStyle(self): return None
    def hasStyleSetting(self, name):
        return self.getStyleSetting(name, None) is not None
    def getStyleSetting(self, name, default=NotImplemented):
        return self.getSpecifiedStyleSetting(name, default)
    def getSpecifiedStyleSetting(self, name, default=NotImplemented):
        return self.getSetting(name, default)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Unraveling related
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def checkUnravel(self, elemBuilder):
        if self.hasSetting('unravel', 1):
            unravel = self.getSetting('unravel').lower()
            if unravel in ['down', 'true', '1']:
                self.unravelDown()
            elif unravel in ['up', '-1']:
                self.unravelUp()
            elif unravel in ['no', 'none', 'false', '0']:
                pass
            else:
                raise RuntimeError('Unknown unravel setting "%s"' % unravel)

    def unravelUp(self):
        unravelStop = bool(int(self.getSetting('unravel-stop', False)))
        if not unravelStop and self.xmlParent() is not None:
            # Recursively unravel the next level up
            return self.xmlParent().unravelUp()
        else:
        # Unravel this node and everything below it
            return self.unravelDown()

    def unravelDown(self):
        # Unravel this node and everything below it
        self.removeFromParent()
        self._unravelCtxVars() # Context Var/Node settings
        self._unravelVars() # remove our hold on any variables

    def _unravelCtxVars(self):
        if self.hasSetting('ctxelem', 1):
            self.delCtxElem()
    def _unravelVars(self):
        self.__dict__.clear()

    def getChildren(self):
        if self._children is None:
            self.setChildren([])
        return self._children
    def setChildren(self, children):
        result = self._children
        self._children = children
        return result

    def addElement(self, element, srcref):
        self.getChildren().append(element)
        self.addCSSElement(element, srcref)
    def removeElement(self, element):
        self.getChildren().remove(element)

    def removeFromParent(self):
        if self.xmlParent():
            self.xmlParent().removeElement(self)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def hasObject(self):
        # don't use getattr because it we want to know about *instance* variables only...
        return '_obj' in self.__dict__
    def getObject(self):
        return self._obj
    def setObject(self, obj):
        self._obj = obj
        self.onSetObject()
    def delObject(self):
        del self._obj
    obj = property(getObject, setObject, delObject)

    def onSetObject(self):
        if self.hasSetting('ctxobj', 1):
            self.setCtxObj()
        if self.hasCtxHostSettings():
            self.pushContext()
            self.setCtxHostObj()

    _elem = None
    def getElement(self):
        if self._elem is None:
            return self.asWeakProxy()
        try: self._elem.asWeakProxy
        except AttributeError:
            return self._elem
        else: return self._elem.asWeakProxy()
    def setElement(self, elem):
        self._elem = elem
    def delElement(self):
        del self._elem
    elem = property(getElement, setElement, delElement)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Context Related Methods
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getURIResolver(self):
        return self.getContext().getURIResolver()

    def getContext(self):
        return self._ctx
    def setContext(self, ctx):
        self._ctx = ctx
    ctx = context = property(getContext) # assignment shouldn't be too convenient
    def getParentContext(self):
        xmlParent = self.xmlParent()
        if xmlParent is None:
            return self.getContext().getRootContext()
        else:
            return xmlParent.getContext()

    def getContextVar(self, name, *args):
        return getattr(self.getContext(), name, *args)
    def setContextVar(self, name, value):
        setattr(self.getContext(), name, value)
    def delContextVar(self, name):
        delattr(self.getContext(), name)

    def pushContext(self, force=False, ctx=None):
        """Adds a context to the stack, if needed or forced."""
        if force or not self._ctxPushed:
            if ctx is None:
                ctx = self.SkinContextFactory(self.getContext())
            self.setContext(ctx)
            self._ctxPushed += 1
        else: 
            ctx = self.getContext()
        return ctx

    def popContext(self, force=False):
        """Removes a context from the stack if owned or forced.
        Returns the 'popped' context."""
        result = self.getContext()
        if not force and not self._ctxPushed:
            raise RuntimeError('Poping a context that was never pushed')
        self.setContext(result.getNextScope())
        self._ctxPushed = max(0, self._ctxPushed - 1)
        return result
        
    def setInitialContext(self):
        if self.hasSetting('ctxelem', 1):
            self.setCtxElem()
        if _boolFromStr(self.getSetting('ctx-push', weakDefault='False')):
            self.pushContext()
        self.setCtxHostElem()

    def setFinalContext(self):
        pass

    def setCtxObj(self):
        if self.hasObject():
            owner, name = self.getSettingAsAddress('ctxobj', useParentContext=True)
            setattr(owner, name, self.getObject())
    def delCtxObj(self):
        if self.hasObject():
            owner, name = self.getSettingAsAddress('ctxobj', useParentContext=True)
            delattr(owner, name)

    def setCtxElem(self):
        owner, name = self.getSettingAsAddress('ctxelem', useParentContext=True)
        setattr(owner, name, self.getElement())
    def delCtxElem(self):
        owner, name = self.getSettingAsAddress('ctxelem', useParentContext=True)
        delattr(owner, name)

    def hasCtxHostSettings(self):
        return bool(self._ctxHostObjNames) or bool(self._ctxHostElemNames)
    def setCtxHostObj(self):
        if self.hasObject():
            for name in self._ctxHostObjNames:
                setattr(self.getContext(), name, self.getObject())
    def setCtxHostElem(self):
        for name in self._ctxHostElemNames:
            setattr(self.getContext(), name, self.asWeakProxy())

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Utility methods
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    #~ Parent Search Patterns ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def iterXMLParents(self, includeSelf=False):
        if includeSelf: 
            current = self
        else: 
            current = self.xmlParent()
        while current:
            yield current
            current = current.xmlParent()

    def findXMLParentFor(self, callable, *args, **kw):
        for each in self.findXMLParentsFor(callable, *args, **kw):
            return each # will find the first one, if it exists
    def findXMLParentsFor(self, callable, *args, **kw):
        for each in self.iterXMLParents():
            result = callable(each, *args, **kw)
            if result not in (False, None):
                yield result

    def findXMLParentOf(self, instance):
        return self.findXMLParentFor(lambda elem: elem.getObject() is instance and elem)
    def findXMLParentOfType(self, *types):
        return self.findXMLParentFor(lambda elem: isinstance(elem, types) and elem)
    def findXMLParentOrObjectOfType(self, *types):
        def _findXMLParentOrObjectOfType(elem):
            if isinstance(elem, types): return elem
            elif isinstance(elem.getObject(), types): return elem.getObject()
        return self.findXMLParentFor(_findXMLParentOrObjectOfType)
    def findXMLParentObjectOfType(self, *types):
        return self.findXMLParentFor(lambda elem: isinstance(elem.getObject(), types) and elem.getObject())
    def findXMLParentOfObjectOfType(self, *types):
        return self.findXMLParentFor(lambda elem: isinstance(elem.getObject(), types) and elem)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Debug
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def debugCtx(self, bPrint=True, leader=''):
        result = self.ctx
        if bPrint:
            ctxrepr = repr(result)
            for l in ctxrepr.split('\n'):
                print '%s%s' % (leader, l)
        return result

    def debugNameStack(self, bPrint=True, leader=''):
        result = reversed([type(n).__name__ for n in self.iterXMLParents(True)])
        if bPrint:
            print '%s%s' % (leader, '>'.join(result))
        return result

