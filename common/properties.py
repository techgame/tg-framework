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

import copy
import weakref

from TG.common import contextApply

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class NamedProperty(object):
    __name__ = None

    def _getPropertyName(self, obj):
        if obj is not None and self.__name__ is None:
            # search the klass namespace for the name of self
            name = self._findNameOfSelfIn(obj.__class__)
            self._setPropertyName(name)
        return self.__name__
    def _setPropertyName(self, name):
        self.__name__ = name

    def _findNameOfSelfIn(self, namespace):
        for name in dir(namespace):
            if getattr(namespace, name) is self:
                return name
        else:
            raise LookupError("Self (%r) not found in namespace (%r)" % (self, namespace))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _getObjAttrName(self, obj, prefixName):
        propertyName = self._getPropertyName(obj)
        if '%s' in prefixName:
            return prefixName % propertyName
        else:
            return prefixName + propertyName

    def _getObjAttr(self, obj, prefixName, *args):
        return getattr(obj, self._getObjAttrName(obj, prefixName), *args)
    def _setObjAttr(self, obj, prefixName, *args):
        return setattr(obj, self._getObjAttrName(obj, prefixName), *args)
    def _delObjAttr(self, obj, prefixName, *args):
        return delattr(obj, self._getObjAttrName(obj, prefixName), *args)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class NamedPropertyEx(NamedProperty):
    _cacheNamePrefix = '__cache_%s'
    _cacheName = None

    def _getCacheName(self, obj=None):
        if obj is not None and self._cacheName is None:
            self._setCacheName(self._getObjAttrName(obj, self._cacheNamePrefix))
        return self._cacheName
    def _setCacheName(self, cacheName):
        self._cacheName = cacheName

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CachedPropertyBase(NamedPropertyEx):
    def __get__(self, obj, klass):
        if obj is not None:
            name = self._getCacheName(obj)
            try: 
                return getattr(obj, name)
            except AttributeError: 
                propObj = self.create(obj, name)
                if propObj is not NotImplemented:
                    return propObj
                else:
                    raise
        else:
            return self

    def __set__(self, obj, value):
        setattr(obj, self._getCacheName(obj), value)

    def __delete__(self, obj):
        delattr(obj, self._getCacheName(obj))

    def create(self, obj, name):
        return NotImplemented

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CopyProperty(CachedPropertyBase):
    _cacheNamePrefix = '__lazy_%s'

    def __init__(self, value):
        self.startValue = value

    def copy(self):
        return copy.copy(self)

    def create(self, obj, name):
        value = self.getValueCopy()
        self.__set__(obj, value)
        return getattr(obj, name)

    def getValueCopy(self):
        return self.startValue.copy()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class LazyProperty(CachedPropertyBase):
    _cacheNamePrefix = '__lazy_%s'
    isObjectProperty = False

    def __init__(self, factory, *args, **kw):
        self.isObjectProperty = kw.pop('isObjectProperty', self.isObjectProperty)
        self.bindFactory(factory, *args, **kw)

    def copy(self):
        return copy.copy(self)

    def bindFactory(self, factory, *args, **kw):
        self.Factory = contextApply.ContextApply_p_s(factory, *args, **kw)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def create(self, obj, name):
        value = self.getDefaultValue(weakref.proxy(obj))
        self.__set__(obj, value)
        return getattr(obj, name)

    def getDefaultValue(self, obj):
        if self.isObjectProperty:
            propObj = self.Factory(obj)
        else:
            propObj = self.Factory()
        self.onCreate(propObj, obj)
        return propObj

    def onCreate(self, propObj, hostObj):
        pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class LazyObjProperty(LazyProperty):
    isObjectProperty = True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ LazyProperty with general decorator support
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class DecoLazyProperty(LazyProperty):
    def copy(self):
        newSelf = LazyProperty.copy(self)
        newSelf._setDecoratorList(self._copyDecoratorList())
        return newSelf

    def create(self, obj, name):
        propObj = LazyProperty.create(self, obj, name)
        self._applyDecoratorList(obj, propObj)
        return propObj

    def _applyDecoratorList(self, obj, propObj):
        for decoItem in self._getDecoratorList():
            self._applyDecorated(obj, propObj, decoItem)

    def _applyDecorated(self, obj, propObj, (applyMethodName, methodName, args, kw)):
        applyMethod = getattr(propObj, applyMethodName)
        objMethod = getattr(obj, methodName)
        applyMethod(objMethod, *args, **kw)

    def _addDecorated(self, applyMethod, hostMethod, *args, **kw):
        if not isinstance(applyMethod, (str, unicode)):
            applyMethod = applyMethod.__name__
        if not isinstance(hostMethod, (str, unicode)):
            hostMethodName = hostMethod.__name__
        else: hostMethodName = hostMethod

        decoItem = (applyMethod, hostMethodName, args, kw)
        self._getDecoratorList().append(decoItem)
        return hostMethod

    def _removeDecoratedByHostMethod(self, hostMethod):
        if not isinstance(hostMethod, (str, unicode)):
            hostMethod = hostMethod.__name__

        dl = [d for d in self._getDecoratorList() if d[1] != hostMethod]
        self._setDecoratorList(dl)
        return None

    def _removeDecoratedByApplyMethod(self, applyMethod):
        if not isinstance(applyMethod, (str, unicode)):
            applyMethod = applyMethod.__name__

        dl = [d for d in self._getDecoratorList() if d[0] != applyMethod]
        self._setDecoratorList(dl)
        return None

    def _removeDecorated(self, applyMethod, hostMethod):
        if not isinstance(applyMethod, (str, unicode)):
            applyMethod = applyMethod.__name__
        if not isinstance(hostMethod, (str, unicode)):
            hostMethod = hostMethod.__name__

        dl = [d for d in self._getDecoratorList() if d[:2] != (applyMethod, hostMethod)]
        self._setDecoratorList(dl)
        return None

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Decorator Action List
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    _decoratorList = None
    def _getDecoratorList(self):
        if self._decoratorList is None:
            self._setDecoratorList([])
        return self._decoratorList
    def _setDecoratorList(self, decoratorList):
        self._decoratorList = decoratorList
    def _delDecoratorList(self):
        self._decoratorList = None
    def _copyDecoratorList(self):
        return self._getDecoratorList()[:]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Property Factory
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class PropertyFactory(object):
    PropertyClass = LazyProperty

    def property(klass, *args, **kw):
        return klass.PropertyClass(klass, *args, **kw)
    property = classmethod(property)
    
    def objProperty(klass, *args, **kw):
        kw['isObjectProperty'] = True
        return klass.property(*args, **kw)
    objProperty = classmethod(objProperty)

