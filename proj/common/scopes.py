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
import chainedDict

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ScopeBase(object):
    __slots__ = ('_nextScope',)
    def getNextScope(self):
        return self._nextScope
    next = getNextScope
    def setNextScope(self, nextScope):
        self._nextScope = nextScope

    def iterScopes(self, includeSelf=True):
        if includeSelf: scope = self
        else: scope = self.getNextScope()
        while scope is not None:
            yield scope
            scope = scope.getNextScope()
    __iter__ = iterScopes

    def rootScope(self):
        for last in self.iterScopes(True): pass
        return last
    root = rootScope

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class StackScopeBase(ScopeBase):
    __slots__ = ()

    def __init__(self, channel=None, frameDepth=1):
        self._linkScopes(channel, frameDepth+1)

    def forChannel(klass, channel=None, frameDepth=1):
        frame = sys._getframe(frameDepth)
        result = klass._nextScopeFromFrame(channel, frame)
        del frame
        return result
    forChannel = classmethod(forChannel)

    def _linkScopes(self, channel, frameDepth):
        frame = sys._getframe(frameDepth)
        frame.f_locals[self._scopeKey(channel)] = self
        self.setNextScope(self._nextScopeFromFrame(channel, frame.f_back))
        del frame

    def _scopeKey(klass, channel):
        return (klass, channel)
    _scopeKey = classmethod(_scopeKey)

    def _nextScopeFromFrame(klass, channel, frame):
        key, result = klass._scopeKey(channel), None

        while frame:
            if key in frame.f_locals:
                result = frame.f_locals[key]
                break
            else:
                frame = frame.f_back

        del frame
        return result
    _nextScopeFromFrame = classmethod(_nextScopeFromFrame)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ScopeAttributeLookupMixin(object):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __repr__(self):
        return "<%s.%s::\n    %s>" % (
            self.__class__.__module__, self.__class__.__name__, 
            ',\n    '.join([repr(vars(each)) for each in self]))

    def __getattr__(self, name):
        try:
            return self.get(name, NotImplemented, False)
        except LookupError, e:
            raise AttributeError(*e.args)

    def __delattr__(self, name):
        owner = self.getOwnerAndValue(name)[0]
        if owner is self:
            object.__delattr__(self, name)
        else:
            delattr(owner, name)

    def getLocalAttr(self, name, default=None):
        return self.__dict__.get(name, default)
    def getLocalAttrFor(self, scope, name, default=None):
        if hasattr(scope, 'getLocalAttr'):
            return scope.getLocalAttr(name, default)
        else:
            return getattr(scope, name, default)

    def get(self, key, default=None, includeSelf=True):
        return self.getOwnerAndValue(key, default, includeSelf)[1]
    def getOwner(self, key, default=None, includeSelf=True):
        return self.getOwnerAndValue(key, default, includeSelf)[0]
    def getOwnerAndValue(self, key, default=None, includeSelf=True):
        sential = object()
        for scope in self.iterScopes(includeSelf):
            result = self.getLocalAttrFor(scope, key, sential)
            if result is not sential:
                return scope, result
        if default is not NotImplemented:
            return None, default
        else:
            raise KeyError, key

    def scopeVars(self):
        result = dict()
        for scope in list(self.iterScopes(True))[::-1]:
            result.update(vars(scope))
        return result
    def itervalues(self): return self.scopeVars().itervalues()
    def iterkeys(self): return self.scopeVars().iterkeys()
    def iteritems(self): return self.scopeVars().iteritems()
    def values(self): return self.scopeVars().values()
    def keys(self): return self.scopeVars().keys()
    def items(self): return self.scopeVars().items()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class LinkedScope(ScopeBase, ScopeAttributeLookupMixin):
    def __init__(self, nextScope=None):
        self.setNextScope(nextScope)

class StackScope(StackScopeBase, ScopeAttributeLookupMixin):
    pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    class TestObject(object):
        def __init__(self):
            self.A()

        def A(self):
            ss = StackScope()
            ss.value = 'A'
            ss.A = "This value was set in 'A'"
            ss.fun = True
            self.B()

        def B(self):
            ss = StackScope('Channel 2')
            ss.B = "B decided it wanted a second channel"
            ss.icky = 1
            self.C()

        def C(self):
            ss = StackScope()
            ss.value = 'C'
            ss.tricky = 3.14
            ss.C = "The method 'C' set this value"
            self.D()

        def D(self):
            chNone = StackScope.forChannel()
            print "Default Channel:"
            print repr(chNone)
            print

            ch2 = StackScope.forChannel('Channel 2')
            print "Channel 2:"
            print repr(ch2)
            print

    r = TestObject()

