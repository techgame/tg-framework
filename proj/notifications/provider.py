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

from TG.common.iterators import ifilter
import engine

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def iProviderFilter(host, results):
    return ifilter(host.getPredicate(), results)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Provider(engine.PlugableNotification):
    """Providers returns the results of the notified functions"""

    notifyEach = staticmethod(engine.notify.yieldNotify)
    filterEach = staticmethod(engine.notify.noFilter)

    def request(self, *args, **kw):
        return self._notify(*args, **kw)

class PredicatedProvider(Provider):
    """Returns the results of the notified functions if they pass the predicate"""
    predicate = None
    filterEach = staticmethod(iProviderFilter)

    def getPredicate(self):
        return self.predicate
    def setPredicate(self, predicate):
        self.predicate = predicate

