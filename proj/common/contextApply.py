#!/usr/bin/env python
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##~ Copyright (C) 2002-2004  TechGame Networks, LLC.
##~ 
##~ This library is free software; you can redistribute it and/or
##~ modify it under the terms of the BSD style License as found in the 
##~ LICENSE file included with this distribution.
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""Binds calling variables to a callable object, with ordering options."""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from bindCallable import WeakBoundCallable, StrongBoundCallable, Curry

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Tuple / Dictionary Join Functions for Smart Apply 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def _joinkw(kw1, kw2):
    """Join two dicts without modifying either."""
    kw = kw2.copy()
    kw.update(kw1)
    return kw

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Default Context Apply Class
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class _StrongContextApply(StrongBoundCallable):
    """Base class for adding positional and keyword based "context" to StrongBoundCallable objects"""

    def __init__(self, callback, *args, **kw):
        StrongBoundCallable.__init__(self, callback)
        self.saveContext(args, kw)

    def saveContext(self, args, kw):
        """Saves extra paramters to be passed to the StrongBoundCallable object.  Creates the "context" part of ContextApply."""
        raise NotImplementedError

class _WeakContextApply(WeakBoundCallable):
    """Base class for adding positional and keyword based "context" to WeakBoundCallable objects"""

    def __init__(self, callback, *args, **kw):
        WeakBoundCallable.__init__(self, callback)
        self.saveContext(args, kw)

    def saveContext(self, args, kw):
        """Saves extra paramters to be passed to the WeakBoundCallable object.  Creates the "context" part of ContextApply."""
        raise NotImplementedError

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ContextApply_p_s_mixin(object):
    """BoundCallable object whose parameters will be "constructed" in the following order:
        - Passed from calling code,
        - Saved context,
    """
    def saveContext(self, args, kw):
        self.args = args
        self.kw = kw

    def __call__(self, *args, **kw):
        return self._doCall(*(args + self.args), **_joinkw(kw, self.kw))

class ContextApply_s_p_mixin(object):
    """BoundCallable object whose parameters will be "constructed" in the following order:
        - Saved context,
        - Passed from calling code,
    """
    def saveContext(self, args, kw):
        self.args = args
        self.kw = kw

    def __call__(self, *args, **kw):
        return self._doCall(*(self.args + args), **_joinkw(self.kw, kw))

class ContextApply_p_mixin(object):
    """BoundCallable object whose parameters will be "constructed" in the following order:
        - Passed from calling code,

    Note: This is the same as calling the BoundCallable directly, but appears here for completeness.
    """
    def saveContext(self, args, kw): pass
    def __call__(self, *args, **kw):
        return self._doCall(*args, **kw)

class ContextApply_s_mixin(object):
    """BoundCallable object whose parameters will be "constructed" in the following order:
        - Saved context,

    Note: The parameters from the calling code will be completely ignored.
    """
    def saveContext(self, args, kw):
        self.args = args
        self.kw = kw

    def __call__(self, *args, **kw):
        return self._doCall(*self.args, **self.kw)

class ContextApply_0_mixin(object):
    """BoundCallable object whose parameters will be "constructed" in the following order:
        - args will be an empty tuple,
        - kw will be an empty dict,

    Note: The parameters from both the calling code and the "context" will be completely ignored.
    """
    def saveContext(self, args, kw): pass
    def __call__(self, *args, **kw):
        return self._doCall()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Coupling of mixin classes to create common templates
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class StrongContextApply_p_s(ContextApply_p_s_mixin, _StrongContextApply): pass
class StrongContextApply_s_p(ContextApply_s_p_mixin, _StrongContextApply): pass
class StrongContextApply_p(ContextApply_p_mixin, _StrongContextApply): pass
class StrongContextApply_s(ContextApply_s_mixin, _StrongContextApply): pass
class StrongContextApply_0(ContextApply_0_mixin, _StrongContextApply): pass

class WeakContextApply_p_s(ContextApply_p_s_mixin, _WeakContextApply): pass
class WeakContextApply_s_p(ContextApply_s_p_mixin, _WeakContextApply): pass
class WeakContextApply_p(ContextApply_p_mixin, _WeakContextApply): pass
class WeakContextApply_s(ContextApply_s_mixin, _WeakContextApply): pass
class WeakContextApply_0(ContextApply_0_mixin, _WeakContextApply): pass

ContextApply_p_s = StrongContextApply_p_s 
ContextApply_s_p = StrongContextApply_s_p 
ContextApply_p = StrongContextApply_p 
ContextApply_s = StrongContextApply_s 
ContextApply_0 = StrongContextApply_0 

WeakContextApply = WeakContextApply_p_s
StrongContextApply = StrongContextApply_p_s
ContextApply = StrongContextApply_p_s

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Bindable Wrappers
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Bindable(object):
    _binding = None

    _contextApply = ContextApply 
    _contextApply_p_s = ContextApply_p_s 
    _contextApply_s_p = ContextApply_s_p 
    _contextApply_p = ContextApply_p 
    _contextApply_s = ContextApply_s 
    _contextApply_0 = ContextApply_0 

    def __call__(self, *args, **kw):
        binding = self.getBinding()
        return binding(*args, **kw)

    def getBinding(self):
        return self._binding
    def setBinding(self, callableBinding):
        self._binding = callableBinding
        return self

    def bind(self, callback, *args, **kw):
        return self.setBinding(self._contextApply(callback, *args, **kw))
    def bind_p_s(self, callback, *args, **kw):
        return self.setBinding(self._contextApply_p_s(callback, *args, **kw))
    def bind_s_p(self, callback, *args, **kw):
        return self.setBinding(self._contextApply_s_p(callback, *args, **kw))
    def bind_s(self, callback, *args, **kw):
        return self.setBinding(self._contextApply_s(callback, *args, **kw))
    def bind_p(self, callback, *args, **kw):
        return self.setBinding(self._contextApply_p(callback, *args, **kw))
    def bind_0(self, callback, *args, **kw):
        return self.setBinding(self._contextApply_0(callback, *args, **kw))

class StrongBindable(Bindable):
    _contextApply = StrongContextApply 
    _contextApply_p_s = StrongContextApply_p_s 
    _contextApply_s_p = StrongContextApply_s_p 
    _contextApply_p = StrongContextApply_p 
    _contextApply_s = StrongContextApply_s 
    _contextApply_0 = StrongContextApply_0 

class WeakBindable(Bindable):
    _contextApply = WeakContextApply 
    _contextApply_p_s = WeakContextApply_p_s 
    _contextApply_s_p = WeakContextApply_s_p 
    _contextApply_p = WeakContextApply_p 
    _contextApply_s = WeakContextApply_s 
    _contextApply_0 = WeakContextApply_0 

