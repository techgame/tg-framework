#!/usr/bin/env python
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

import sys
import weakref

from itertools import count
from TG.notifications.event import Event

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Version Bases
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class VersionIter(object):
    def __init__(self, node, fromVersion=None):
        self._node = node
        if fromVersion is not None:
            self.setVersion(fromVersion)
    
    def __nonzero__(self):
        return self.getVersion() < self.getNode().getVersion()

    _node = None
    def getNode(self):
        return self._node
    def setNode(self, node):
        self._node = node

    def getNodeIter(self):
        node = self.getNode()
        return node.iterVersions(self.getVersion()), node.getVersion()

    _version = 0
    def getVersion(self):
        return self._version
    def setVersion(self, version):
        self._version = version

    def __iter__(self):
        return self

    def iterByN(self, n):
        return (self.next() for i in xrange(n))

    def next(self, default=None):
        iter, maxVersion = self.getNodeIter()
        for v,i in iter:
            self.setVersion(v+1)
            return i
        else:
            self.setVersion(maxVersion)
            raise StopIteration()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Version Node
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class VersionNode(object):
    VersionStoreFactory = dict
    VersionIterFactory = VersionIter
    _sentinal = object()

    _vStore = None
    def getVersionStore(self):
        if self._vStore is None:
            self.createVersionStore()
        return self._vStore
    def setVersionStore(self, vStore):
        self._vStore = vStore
    def createVersionStore(self):
        self.setVersionStore(self.VersionStoreFactory())

    _version = 0
    def getVersion(self):
        return self._version
    def nextVersion(self):
        v = self._version
        self._version = v+1
        return v

    def iter(self, n=0):
        return self.VersionIterFactory(self, n)

    def iterVersions(self, fromVersion=None):
        sentinal = self._sentinal
        currentVersion = self.getVersion()

        if fromVersion is None: 
            fromVersion = 0
        elif fromVersion < 0:
            fromVersion = max(0, fromVersion + currentVersion)
        else:
            fromVersion = min(fromVersion, currentVersion)

        vStore = self.getVersionStore()
        for version in count(fromVersion):
            # We could use xrange except that the upper bound may be increased
            # while we are in the iterator.  So keep checking against the top
            # bound on misses
            item = vStore.get(version, sentinal)
            if item is not sentinal:
                item = self._wrapItem(item)
                yield version, item()

            elif version > self.getVersion():
                break

    def _wrapItem(self, item):
        return (lambda: item)

    def add(self, item):
        result = self._addBasic(item)
        self._onAddItem(item)
        return result

    def _addBasic(self, item):
        self._discardExistingVersions(item)
        versionTag = self.nextVersion()
        vStore = self.getVersionStore()
        vStore[versionTag] = item
        return True

    def update(self, items):
        for item in items:
            self.add(item)

    def discard(self, item):
        if self._discardBasic(item):
            self._onDiscardItem(item)
            return True
        return False

    def _discardBasic(self, item):
        sentinal = self._sentinal
        vStore = self.getVersionStore()
        keys = [k for k, v in vStore.iteritems() if v is item]

        for k in keys:
            vStore.pop(k)

        return bool(keys)

    def _discardExistingVersions(self, item):
        pass

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _onAddItem(self, item):
        pass
    def _onDiscardItem(self, item):
        pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class WeakVersionNode(VersionNode):
    VersionStoreFactory = weakref.WeakValueDictionary

    def _wrapItem(self, item):
        try: 
            return weakref.ref(item)
        except TypeError: 
            return lambda: item

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Version Event Mixins
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class VersionEventMixin(object):
    onAdd = Event.objProperty()
    onDiscard = Event.objProperty()

    def _onAddItem(self, item):
        self.onAdd(item)
    def _onDiscardItem(self, item):
        self.onDiscard(item)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Version Nodes
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class VersionEventNode(VersionEventMixin, VersionNode):
    pass

class WeakVersionEventNode(VersionEventMixin, WeakVersionNode):
    pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    import weakref
    class VTestNode(WeakVersionNode):
        def __init__(self, ns, parent):
            self.ns = ns

        def __repr__(self):
            return self.ns

    class CharWrapper(object):
        def __init__(self, x):
            self.c = chr(x)
        def __del__(self):
            print 'BYE:', self
        def __repr__(self):
            return self.c

    tg = VTestNode('TG', None)
    
    wrappers = []
    for x in xrange(ord('a'), ord('z')+1):
        c = CharWrapper(x)
        wrappers.append(c)
        tg.add(c)

    print 
    v = 0
    verIter = tg.iter()
    for x in xrange(20):
        for e in verIter.iterByN(4):
            print e
            del e
        del wrappers[:6]


