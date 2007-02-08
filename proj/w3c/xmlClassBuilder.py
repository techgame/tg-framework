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

import sys
import keyword
import xmlBuilder

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ElementFactoryError = xmlBuilder.ElementFactoryError

class XMLFactory(object):
    def xmlnsFromName(moduleName):
        moduleName = moduleName.replace('.__init__', '')
        return moduleName
    xmlnsFromName = staticmethod(xmlnsFromName)

    class Collection(dict):
        next = None

        def __repr__(self):
            return '<%s.%s \'%s\'>' % (XMLFactory.__name__, self.__class__.__name__, self.getName())

        def getElementFactory(self, owner, parent, node, attributes, namespacemap):
            try:
                for idx in self._getElementFactoryIndices(node):
                    FactoryFactory = self.get(idx)
                    if FactoryFactory is not None:
                        result = FactoryFactory(owner, parent, node, attributes, namespacemap)
                        if result: 
                            return result
            except XMLFactory.InheritFromNextFactory, (args, kw):
                if self.next is not None:
                    return self.next.getElementFactory(*args, **kw)
            raise ElementFactoryError("Could not find a class to build for node %r" % (node,))

        def addFactory(self, key, xmlfactory):
            if isinstance(key, basestring):
                key = (key,)
            elif isinstance(key, tuple) and not (0 < len(key) <= 2):
                # trim out common usecase of __name__ when packaged for zipimport
                raise ValueError('Invalid factory key: %r' % (key,))

            self[key] = xmlfactory

        def copy(self):
            result = self.__class__(dict.copy(self))
            result.__dict__ = self.__dict__.copy()
            return result

        def setName(self, name):
            self.name = str(name)
            return self
        def getName(self):
            return getattr(self, 'name', '???')

        def getNext(self):
            return self.next
        def setNext(self, factoryCollection):
            if factoryCollection is not self:
                self.next = factoryCollection
            return self

        def pushNext(self, factory):
            if self.getNext() is None: result = self
            else: result = self.copy()
            return result.setNext(factory)

        def popNext(self):
            result = self.getNext()
            self.setNext(None)
            return result

        def _getElementFactoryIndices(self, node):
            if node:
                return tuple(node), tuple(node[:-1]), (None, node[-1]), None
            else: return None

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Specific Factories
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    class FactoryBase(object):
        def __call__(self, *args, **kw):
            return self.getFactory(*args, **kw)

    class InheritFromNextFactory(Exception):
        def __call__(self, *args, **kw):
            raise self.__class__, (args, kw)
    InheritFromNext = InheritFromNextFactory

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    class FromClassmethod(FactoryBase):
        def __init__(self, nextFactory, name='fromXMLBuilder'):
            self.nextFactory = nextFactory
            self.name = name
        def getFactory(self, *args, **kw):
            result = self.nextFactory.getFactory(*args, **kw)
            result = getattr(result, self.methodName)
            return result

    class Static(FactoryBase):
        def __init__(self, result):
            self.result = result
        def getFactory(self, *args, **kw):
            return self.result

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    class Raise(FactoryBase):
        def __init__(self, exception=ElementFactoryError, message=''):
            self.exception = exception
            self.message = message

        def getFactory(self, *args, **kw):
            raise self.exception, self.message

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    class BaseImport(FactoryBase):
        retryimport = True

        def __init__(self, pyPathRoot=''):
            self.pyPathRoot = pyPathRoot
            self._CachedElementFactories = {}

        def isEnabled(self):
            try:
                return self._enabled
            except AttributeError:
                try: 
                    __import__(self.pyPathRoot, {}, {})
                except ImportError:
                    self._enabled = False
                else:
                    self._enabled = True
                return self._enabled

        def _import(self, pyPath, name):
            if not self.isEnabled(): 
                raise ImportError, 'Import element finder %r is disabled because root %r cannot be imported' % (self, self.pyPathRoot)
            name = name.replace('-', '_')
            pyPath = pyPath.replace('-', '_')

            if self.pyPathRoot and pyPath:
                impPath = '.'.join((self.pyPathRoot, pyPath))
            elif not pyPath:
                impPath = self.pyPathRoot
            module = __import__(impPath, {}, {}, name)
            return self._getNameFromModule(module, name)

        def _getNameFromModule(self, module, name):
            try:
                return getattr(module, name)
            except AttributeError:
                if self.retryimport:
                    module = reload(module)
                    try: return getattr(module, name)
                    except AttributeError: pass
                raise ElementFactoryError('Could not find "%s" in module %r' % (name, module))

        def getFactory(self, owner, parent, node, attributes, namespacemap):
            result = self._CachedElementFactories.get(node, None)
            if not result: 
                ns, name = node
                if keyword.iskeyword(name): name = name + '_'
                result = self._import('', name)

                ## The following works for another scheme
                ##result = self.DoImport(*node)

                self._CachedElementFactories[node] = result
            return result

    class HierarchyBaseImport(BaseImport):
        def __init__(self, pyPathRoot='', subpackages=('')):
            super(XMLFactory.HierarchyBaseImport, self).__init__(pyPathRoot)
            self.subpackages = subpackages

        def _import(self, pyPath, name):
            if not self.isEnabled(): 
                raise ImportError('Import element finder %r is disabled because root %r cannot be imported' % (self, self.pyPathRoot))
            name = name.replace('-', '_')
            pyPath = pyPath.replace('-', '_')

            for subPath in self.subpackages:
                if subPath: 
                    impPath = '.'.join((self.pyPathRoot, subPath, pyPath))
                else: 
                    impPath = '.'.join((self.pyPathRoot, pyPath))

                try: 
                    module = __import__(impPath, {}, {}, name)
                except ImportError, e: 
                    notFoundError = sys.exc_info()[2].tb_next is not None
                    if notFoundError:
                        raise
                else: 
                    break
            else:
                raise ImportError("Could not find skin module for '%s' in '%s' or sub-packages %r" % (pyPath, self.pyPathRoot, self.subpackages))

            return self._getNameFromModule(module, name)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    class StaticImport(BaseImport):
        def __init__(self, pyPath, name, *args, **kw):
            XMLFactory.BaseImport.__init__(self, pyPath)
            self.name = name
            self.result = None

        def getFactory(self, *args, **kw):
            if not self.result:
                self.result = self._import('', self.name)
            return self.result
            
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    class NodeImport(BaseImport):
        def getFactory(self, owner, parent, node, attributes, namespacemap):
            result = self._CachedElementFactories.get(node, None)
            if not result: 
                ns, name = node
                if keyword.iskeyword(name): name = name + '_'
                result = self._import(name, name)

                ## The following works for another scheme
                ##result = self.DoImport(*node)

                self._CachedElementFactories[node] = result
            return result
            
    class HierarchyNodeImport(HierarchyBaseImport, NodeImport):
        pass

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    class NamespaceImport(BaseImport):
        def getFactory(self, owner, parent, node, attributes, namespacemap):
            result = self._CachedElementFactories.get(node, None)
            if not result: 
                ns, name = node
                if keyword.iskeyword(name): name = name + '_'
                result = self._import('%s.%s' % (ns, name), name)

                ## The following works for another scheme
                ##result = self.DoImport(*node)

                self._CachedElementFactories[node] = result
            return result

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    class TryList(FactoryBase):
        def __init__(self, trylist, ignoreExceptions=[ElementFactoryError, ImportError]):#, AttributeError, KeyError]):
            self._trylist = trylist
            self._ignoreExceptions = tuple(ignoreExceptions)

        def getFactory(self, owner, parent, node, attributes, namespacemap):
            for each in self._trylist:
                try:
                    return each(owner, parent, node, attributes, namespacemap)
                except self._ignoreExceptions:
                    pass

            raise ElementFactoryError('No suitable element factory for node %r' % (node,))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    class CachedTryList(TryList):
        def __init__(self, *args, **kw):
            XMLFactory.TryList.__init__(self, *args, **kw)
            self._CachedElementFactories = {}

        def getFactory(self, owner, parent, node, attributes, namespacemap):
            result = self._CachedElementFactories.get(node, None)
            if result: 
                return result
            for each in self._trylist:
                try:
                    result = each(owner, parent, node, attributes, namespacemap)
                    self._CachedElementFactories[node] = result
                    return result
                except self._ignoreExceptions, e:
                    pass

            raise ElementFactoryError('No suitable element factory for node %r' % (node,))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Class Builders
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ClassBuilderState(xmlBuilder.BuilderState):
    def __init__(self, xmlbuilder):
        xmlBuilder.BuilderState.__init__(self, xmlbuilder)
        self._xmlFactories = xmlbuilder.xmlFactories

    def restore(self, xmlbuilder):
        xmlbuilder.xmlFactories = self._xmlFactories
        return xmlBuilder.BuilderState.restore(self, xmlbuilder)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class XMLClassBuilder(xmlBuilder.XMLBuilder):
    xmlFactories = XMLFactory.Collection()
    BuilderStateFactory = ClassBuilderState

    def getElementFactory(self, *args, **kw):
        return self.xmlFactories.getElementFactory(*args, **kw)

    def pushXMLFactories(self, xmlFactories):
        self.xmlFactories = xmlFactories.pushNext(self.xmlFactories)

    def popXMLFactories(self):
        result = self.xmlFactories
        self.xmlFactories = self.xmlFactories.popNext()
        if self.xmlFactories is None:
            raise Exception("Popped last XMLFactory off stack! Last: %r" % (result,))
        return result

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ClassElementBase(xmlBuilder.ElementBase):
    def xmlChildFactory(self, elemBuilder, parentElem, node, attributes, namespaceMap):
        """This gets called so that elements may override the factory for their direct children"""

class XMLClassObjectBuilder(XMLClassBuilder):
    def getElementFactory(self, *args, **kw):
        if self.elementStack:
            # give the element a shot at providing the factory
            result = self.elementStack.topElement().xmlChildFactory(*args, **kw)
            if result is not None: 
                return result
        return XMLClassObjectBuilder.getElementFactory(*args, **kw)

