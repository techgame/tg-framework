##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~ Copyright (C) 2002-2005  TechGame Networks, LLC.              ##
##~                                                               ##
##~ This library is free software; you can redistribute it        ##
##~ and/or modify it under the terms of the BSD style License as  ##
##~ found in the LICENSE file included with this distribution.    ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import weakref
from TG.notifications.event import Event

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class WeakValueDict(weakref.WeakValueDictionary):
    pass

class WeakValueEventDict(WeakValueDict):
    onWeakRemove = Event.property()

    def __init__(self, *args, **kw):
        weakref.WeakValueDictionary.__init__(self, *args, **kw)
        def remove(wr, selfref=weakref.ref(self)):
            self = selfref()
            if self is not None:
                self._onWeakRemove(wr.key)
        self._remove = remove

    def _onWeakRemove(self, key):
        del self.data[key]
        self.onWeakRemove(key)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class WeakKeyDict(weakref.WeakKeyDictionary):
    pass
class WeakKeyEventDict(WeakKeyDict):
    onWeakRemove = Event.property()

    def __init__(self, *args, **kw):
        weakref.WeakValueDictionary.__init__(self, *args, **kw)
        def remove(key, selfref=weakref.ref(self)):
            self = selfref()
            if self is not None:
                self._onWeakRemove(key)
        self._remove = remove

    def _onWeakRemove(self, key):
        del self.data[key]
        self.onWeakRemove(key)

