#!/usr/bin/env python
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##~ Copyright (C) 2002-2004  TechGame Networks, LLC.
##~ 
##~ This library is free software; you can redistribute it and/or
##~ modify it under the terms of the BSD style License as found in the 
##~ LICENSE file included with this distribution.
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Simple implementations
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def simpleNotify(_sinks_, *args, **kw):
    """Simply iterates through the sinks, calling each one"""
    for each in _sinks_:
        each(*args, **kw)

def listNotify(_sinks_, *args, **kw):
    """Iterates through the sinks, calling each one and keeping the result in a list"""
    return [each(*args, **kw) for each in _sinks_]

def yieldNotify(_sinks_, *args, **kw):
    """Yields the result of each sink call.  

    NOTE: May cause interference with locking mechanism because of the delayed evaluation.
    """
    for each in _sinks_:
        yield each(*args, **kw)

def noFilter(_host_, results):
    return results

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Notify Mixin Strategies
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class NotifyBase(object):
    def _notifySinks(self, *args, **kw):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

class SimpleNotify(NotifyBase):
    _notifySinks = simpleNotify

class ListNotify(NotifyBase):
    _notifySinks = listNotify

class GeneratorNotify(NotifyBase):
    _notifySinks = yieldNotify

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class PlugableNotify(NotifyBase):
    notifyEach = staticmethod(simpleNotify)
    filterEach = staticmethod(noFilter)

    def _notifySinks(self, *args, **kw):
        sinks = self.getSinks()

        strategy = self.getNotifyStrategy()
        result = strategy(sinks, *args, **kw)

        filterEach = self.getFilterStrategy()
        return filterEach(self, result)

    def getNotifyStrategy(self):
        return self.notifyEach
    def setNotifyStrategy(self, strategy):
        if not callable(strategy):
            raise ValueError("Expected a callable object for the notify strategy")
        self.notifyEach = strategy

    def getFilterStrategy(self):
        return self.filterEach
    def setFilterStrategy(self, strategy):
        if not callable(strategy):
            raise ValueError("Expected a callable object for the filter strategy")
        self.filterEach = strategy

