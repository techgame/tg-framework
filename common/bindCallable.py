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

import weakref
import types

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

typesBindMethods = (types.MethodType, types.BuiltinMethodType )
typesInstances = (types.ObjectType, types.InstanceType)
typesRequireBinding = typesBindMethods + typesInstances

typesNonBindMethods = (types.FunctionType, types.LambdaType, types.GeneratorType, types.BuiltinFunctionType)
typesNonBind = typesNonBindMethods + (types.ClassType, types.ModuleType)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Callable Aspects
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class BoundCallableBase(object):
    """Ultimate baseclass of BoundCallable objects.  Derive from this object if the class 
    handles references to itself, by itself."""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class WeakBoundCallable(BoundCallableBase):
    """weakref for callable objects.
    
    Weakref objects have become a matter of necessity for managing the scope of interconnected
    networks of objects, defining owner and owned, while still allow for reference loops.
    However, weakref-ing a bound method always returns a dead weakref, but true references keep
    the "owner" class around.  WeakBoundCallable's intention is to provide weakref-type support 
    for bound methods, as well as all other callable objects.
    
    As a related sidenote, the ContextApply module builds upon this concepts to bind method variables
    to bound-callable objects.
    
    """
    
    im_self = None
    im_func = None

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Special 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __init__(self, Callable, *weakrefArgs, **weakrefKw):
        if Callable is None: 
            # A "None" method... it should expire immediately
            pass
        elif isinstance(Callable, BoundCallableBase):
            # One of those weird instances where we are proxying for an object very similar to ourself... 
            # keep a hard reference to the BoundCallableBase
            self.im_func = Callable
        elif isinstance(Callable, typesBindMethods):
            # Wrap up the method and potential instance
            self.im_func = getattr(Callable, 'im_func', Callable)
            if getattr(Callable, 'im_self', None) is not None: 
                self.im_self = weakref.ref(Callable.im_self, *weakrefArgs, **weakrefKw)
            else:
                pass
        elif isinstance(Callable, typesInstances):
            # This is a "callable object", make a weakref to it
            self.im_self = weakref.ref(Callable, *weakrefArgs, **weakrefKw)
            self.im_func = None
        elif callable(Callable):
            # What the heck is it?  well... its supposed to be callable...
            self.im_func = Callable

    def __repr__(self):
        return "<%s.%s on: %r to: %r>" % (self.__class__.__module__, self.__class__.__name__, self.im_self, self.im_func)

    def __nonzero__(self):
        if self.im_self is not None:
            return self.im_self() is not None and 1 or 0
        else: 
            return self.im_func and 1 or 0

    def __hash__(self):
        if self.im_self is not None:
            return hash(self.im_self)
        else: 
            return hash(self.im_func)

    def __eq__(self, other):
        if isinstance(other, WeakBoundCallable):
            return (self.im_self == other.im_self) and (self.im_func == other.im_func) 
        elif isinstance(other, weakref.ReferenceType): 
            return self.im_func == other or self.im_self == other
        elif callable(other): 
            return self == WeakBoundCallable(other)
        else: return self is other

    def __ne__(self, other):
        return not self.__eq__(other)

    def _doCall(self, *args, **kw):
        if self.im_self:
            im_self = self.im_self()
            if im_self is not None: 
                if self.im_func:
                    return self.im_func(im_self, *args, **kw)
                else: return im_self(*args, **kw)
            else: raise weakref.ReferenceError, "weakly-referenced object no longer exists"
        else: return self.im_func(*args, **kw)

    #def __call__(self, *args, **kw):
    #    return self._doCall(args, kw)
    __call__ = _doCall

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

BoundCallable = WeakBoundCallable

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class StrongBoundCallable(BoundCallableBase):
    """Provides the same interface as WeakBoundCallable, but maintains strong references
    to both class instances and callable objects.  Used mainly in ContextApply to build 
    upon a common class interface.
    """

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Special 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __init__(self, Callable):
        self.im_func = Callable

    def __repr__(self):
        return "<%s.%s to: %r>" % (self.__class__.__module__, self.__class__.__name__, self.im_func)

    def __nonzero__(self):
        return self.im_func is not None and 1 or 0

    def __hash__(self):
        return hash(self.im_func)

    def __eq__(self, other):
        if isinstance(other, StrongBoundCallable):
            return self.im_func == other.im_func
        elif callable(other): 
            return self == StrongBoundCallable(other)
        else: return self is other

    def __ne__(self, other):
        return not self.__eq__(other)

    def _doCall(self, *args, **kw):
        return self.im_func(*args, **kw)

    #def __call__(self, *args, **kw):
    #    return self._doCall(args, kw)
    __call__ = _doCall

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Curry(StrongBoundCallable):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Special 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __init__(self, callback, *args, **kw):
        StrongBoundCallable.__init__(self, callback)
        self.args = args
        self.kw = kw

    def __call__(self, *args, **kw):
        return self._doCall(*self.args, **self.kw)

    #~ tuple form ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def asTuple(self):
        return (self.im_func, self.args, self.kw)

    def fromTuple(klass, curryTuple):
        call, args, kw = curryTuple + ((), {})[len(currytyple)-1:]
        return klass(call, *args, **kw)
    fromTuple = classmethod(fromTuple)

    def callTuple(curryTuple):
        call, args, kw = curryTuple + ((), {})[len(currytyple)-1:]
        return call(*args, **kw)
    callTuple = staticmethod(callTuple)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def bindCallableEx(Callable, BindClass=BoundCallable, *args, **kw):
    """Binds a callable object using BindClass only if needed.""" 
    if isinstance(Callable, BoundCallableBase):
        # It's already bound in some form or another, 
        # but we have to guard it from being wrapped
        # again, because it is itself an instance.
        return Callable
    elif isinstance(Callable, typesNonBind):
        # Doesn't need to be bound
        return Callable
    elif isinstance(Callable, typesRequireBinding):
        # Well if it requires binding, then we should do so!
        return BindClass(Callable, *args, **kw)
    else:
        # not quite sure what it is, but it does not require binding
        return Callable

def bindCallable(Callable, *args, **kw):
    return bindCallableEx(Callable, BoundCallable, *args, **kw)
bind = bindCallable

def weakBindCallable(Callable, *args, **kw):
    """Weakly binds a callable object only if needed."""
    return bindCallableEx(Callable, WeakBoundCallable, *args, **kw)
weakBind = weakBindCallable

def strongBindCallable(Callable, *args, **kw):
    """Strongly binds a callable object only if needed."""
    return bindCallableEx(Callable, StrongBoundCallable, *args, **kw)
strongBind = strongBindCallable

def curryCallable(Callable, *args, **kw):
    """Binds a curry object if needed"""
    if args or kw:
        return Curry(Callable, *args, **kw)
    else: return Callable
curry = curryCallable

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Testing 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    print "Testing..."
    import sys

    class _Test:
        def you(self):
            return self
        def me(self):
            return self
    
    def onrelease(wr):
        print "Released wr:", wr

    a = _Test()
    assert(sys.getrefcount(a) == 2)

    b1 = weakBindCallable(a.me, onrelease)
    assert(b1)
    assert(sys.getrefcount(a) == 2)

    b2 = weakBindCallable(a.me, onrelease)
    assert(b2)
    assert(sys.getrefcount(a) == 2)

    assert(b1 == b2)
    assert(sys.getrefcount(a) == 2)

    assert(a.me == b1)
    assert(a.me == b2)
    assert(b1 == b2)
    assert(b2 == b1)

    b3 = weakBindCallable(a.you, onrelease)
    assert(not b1 == b3)
    assert(b1 != b3)

    del a

    try:
        b1()
        assert(0, "Shouldn't ever get here")
    except weakref.ReferenceError:
        pass

    try:
        if b2:
            b2()
            assert(0, "Shouldn't ever get here")
    except weakref.ReferenceError:
        assert(0, "Shouldn't ever get here")

    print "Test complete."
