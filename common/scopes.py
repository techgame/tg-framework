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
        last = None
        for last in self.iterScopes(True): 
            pass
        return last
    root = rootScope

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def iterFrames(depth=0):
    f = sys._getframe(depth+1)
    while f is not None:
        yield f
        f = f.f_back

class StackScopeBase(ScopeBase):
    __slots__ = ['_channel_']

    iterFrames = staticmethod(iterFrames)

    def __init__(self, channel=None, frameDepth=1):
        self._channel_ = channel
        self._linkScopes(channel, frameDepth+1)

    def forChannel(klass, channel=None, frameDepth=1):
        return klass._nextScopeFromFrame(channel, klass.iterFrames(frameDepth+1))
    forChannel = classmethod(forChannel)

    def top(self, frameDepth=1):
        return self.forChannel(self._channel_, frameDepth+1)
    def push(self, frameDepth=1):
        klass = type(self)
        return klass(self._channel_, frameDepth+1)

    def _linkScopes(self, channel, frameDepth=1):
        iterFrames = self.iterFrames(frameDepth)
        for frame in iterFrames:
            frame.f_locals[self._scopeKey(channel)] = self
            del frame
            break
        self.setNextScope(self._nextScopeFromFrame(channel, iterFrames))

    def _scopeKey(klass, channel):
        return channel
    _scopeKey = classmethod(_scopeKey)

    def _nextScopeFromFrame(klass, channel, iterFrames):
        key = klass._scopeKey(channel)
        missing = object()
        for frame in iterFrames:
            result = frame.f_locals.get(key, missing)
            if result is not missing:
                return result
        else: 
            return None
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
            return self.getAtName(name, NotImplemented, False)
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

    def getAtName(self, key, default=None, includeSelf=True):
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
    def A():
        ss = StackScope()
        ss.value = 'A'
        ss.A = "This value was set in 'A'"
        ss.fun = True
        return B()

    def B():
        ss = StackScope('Channel 2')
        ss.B = "B decided it wanted a second channel"
        ss.icky = 1
        return C()

    def C():
        ss = StackScope()
        ss.value = 'C'
        ss.tricky = 3.14
        ss.C = "The method 'C' set this value"
        return D()

    def D():
        chNone = StackScope.forChannel()
        ch2 = StackScope.forChannel('Channel 2')
        return dict(chNone.items()), dict(ch2.items())

    cnTest = dict(
        A="This value was set in 'A'",
        fun=True,
        value='C',
        tricky=3.14,
        C = "The method 'C' set this value",
        )

    c2Test = dict(
        B="B decided it wanted a second channel",
        icky=1,
        )

    cn, c2 = A()
    assert cn == cnTest, cn
    assert c2 == c2Test, c2

    from pprint import pprint
    print
    print "Passed!"
    print
    print "Default Channel:"
    pprint(cn)
    print
    print "Channel 2:"
    pprint(c2)
    print

