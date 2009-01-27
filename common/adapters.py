#!/usr/bin/env python
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##~ Copyright (C) 2002-2004  TechGame Networks, LLC.
##~ 
##~ This library is free software; you can redistribute it and/or
##~ modify it under the terms of the BSD style License as found in the 
##~ LICENSE file included with this distribution.
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
Breeding of facets, interface, protocols and adaption.  Not quite sure what it is yet!  ;)
"""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def isClassicClass(klass):
    return klass.__name__ == 'classobj'
def isClassicInstance(obj):
    klass = type(obj)
    return isClassicClass(klass)

def isNewStyleClass(klass):
    return klass.__name__ != 'classobj'
def isNewStyleInstance(obj):
    klass = type(obj)
    return isNewStyleClass(klass)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class AdaptionError(Exception):
    formatStr = "Object type %(objType)r does not support protocol %(protocol)r"
    objType = None
    protocol = None

    def __init__(self, obj, protocol, formatStr=None):
        Exception.__init__(self)
        self.objType = type(obj)
        self.protocol = protocol
        if formatStr is not None:
            self.formatStr = formatStr

    def __str__(self):
        return self.formatStr % vars(self)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Adapter(object):
    """Adapts instance 'obj' to based on context in 'protocol'
    
    Note: The intention of adapters is that *both* callables and Adapter
    subclasses are allowable"""

    def __call__(self, obj, protocol, **kw):
        return self.adapt(obj, protocol, **kw)
    def adapt(self, obj, protocol, **kw):
        raise NotImplementedError('Subclass Responsibility')

def isInstanceAdapter(obj, protocol):
    """Adaptors using isinstance() -- probably the most common case"""
    if isinstance(obj, protocol.interface):
        return obj
    else:
        return None

def raiseAdaptionError(obj, protocol):
    raise AdaptionError(obj, protocol)

def noAdaption(obj, protocol):
    return None

class CompositAdapter(Adapter):
    notFoundAdapter = staticmethod(noAdaption)
    _collection = None
    CollectionFactory = list

    def adapt(self, obj, protocol, **kw):
        for adapter in self.iterAdapters():
            result = adapter(obj, protocol, **kw)
            if result is not None:
                break
        else:
            result = self.notFoundAdapter(obj, protocol)
        return result

    def iterAdapters(self):
        return iter(self.getCollection())

    def getCollection(self):
        if self._collection is None:
            self.createCollection()
        return self._collection
    def setCollection(self, collection):
        self._collection = collection
    def createCollection(self):
        collection = self.CollectionFactory()
        self.setCollection(collection)
        return collection

    def add(self, adapter):
        self.getCollection().append(adapter)
    def remove(self, adapter):
        self.getCollection().remove(adapter)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Protocol Binding -- context for adapters
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Protocol(object):
    """Protocol for "dynamic isinstance" functionality"""
    AdapterFactory = CompositAdapter
    _adapter = None 

    def __init__(self, *args, **kw):
        self.context(*args, **kw)

    def __repr__(self):
        return "<%s.%s: %r>" % (self.__class__.__module__, self.__class__.__name__, self.__doc__.split('\n', 1)[0])

    def _getDoc(self):
        return self.__doc__
    def _setDoc(self, doc):
        self.__doc__ = doc
    doc = property(_getDoc, _setDoc)

    def context(self, *args, **kw):
        for n,v in kw.items():
            setattr(self, n, v)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __call__(self, obj, **kw):
        """Alias for .adapt()"""
        return self.adapt(obj, **kw)
    def adapt(self, obj, **kw):
        """Plugable pattern"""
        adapter = self.getAdapter()
        return adapter(obj, self, **kw)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getAdapter(self):
        if self._adapter is None:
            self.createAdapter()
        return self._adapter
    def setAdapter(self, adapter):
        self._adapter = adapter
    adapter = property(getAdapter, setAdapter)

    def createAdapter(self):
        adapter = self.AdapterFactory()

        aSetupAdapter = self.setupAdapter(adapter)
        if aSetupAdapter is not None:
            adapter = aSetupAdapter

        self.setAdapter(adapter)
        return adapter

    def setupAdapter(self, adapter):
        """Override this to setup the new adapter created from the adapterFactory"""
        return adapter

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    class ITest(object): pass
    class Classic: pass

    ITestProtocol = Protocol(interface=ITest, doc='ITest protocol')
    ITestProtocol.adapter.add(isInstanceAdapter)

    strProtocol = Protocol(interface=str, doc='str protocol')
    strProtocol.adapter.add(isInstanceAdapter)
    strProtocol.adapter.add(lambda obj, protocol: str(obj))

    objProtocol = Protocol(interface=object, doc='object protocol')
    objProtocol.adapter.add(isInstanceAdapter)

    classicProtocol = Protocol(doc='Classic protocol test')
    classicProtocol.adapter.add(lambda obj, protocol: (None, obj)[isClassicInstance(obj)])

    newStyleProtocol = Protocol(doc='NewStyle protocol test')
    newStyleProtocol.adapter.add(lambda obj, protocol: (None, obj)[isNewStyleInstance(obj)])

    typeProtocol = Protocol(doc='type protocol test')
    typeProtocol.adapter.add(lambda obj, protocol: (None, obj)[isinstance(obj, type)])

    newStyleWithExceptionProtocol = Protocol(doc='NewStyle protocol (with exception) test')
    newStyleWithExceptionProtocol.adapter.add(lambda obj, protocol: (None, obj)[isNewStyleInstance(obj)])
    newStyleWithExceptionProtocol.adapter.notFoundAdapter = raiseAdaptionError

    testProtocols = [
        objProtocol,
        strProtocol,
        ITestProtocol,
        classicProtocol,
        newStyleProtocol,
        typeProtocol,
        ]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    testObjects = [str, 'stuff', int, 42, Classic, Classic(), ITest, ITest()]

    print
    for protocol in testProtocols:
        print "Adapting: %r(obj)" % (protocol,)
        for obj in testObjects: 
            print "   %-60r:" % (obj,),
            print repr(protocol(obj))
        print
    print

    for protocol in [newStyleWithExceptionProtocol,]:
        print "Adapting: %r(obj)" % (protocol,)
        for obj in testObjects: 
            print "   %-60r:" % (obj,),
            if isinstance(obj, type(Classic)):
                try:
                    print repr(protocol(obj))
                except AdaptionError:
                    print
                    print
                    print "Expected exception caught: (a good and planned thing)"
                    print "  %r does not support %r" % (obj, protocol)
                    print
                else:
                    assert False, "Object %r is NOT supposed to support %r" % (obj, protocol)
            else:
                print repr(protocol(obj))
        print
    print
