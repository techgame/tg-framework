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

import heapq
import time

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class HeapQueue(object) :
    _heap = None
    def getHeap(self):
        if self._heap is None:
            self._heap = []
        return self._heap

    _heappop = staticmethod(heapq.heappop)
    _heappush = staticmethod(heapq.heappush)
    _heapify = staticmethod(heapq.heappush)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __len__(self):
        return len(self.getHeap())

    def append(self, index, item):
        self._heappush(self.getHeap(), (index, item))

    def popItems(self, index):
        return list(self.iterPopItems(index))
    def iterPopItems(self, index):
        heap = self.getHeap()
        while heap and heap[0][0] < index:
            yield self._heappop(self.getHeap())

    def nextIndex(self):
        heap = self.getHeap()
        if heap:
            return heap[0][0]
        else:
            return None

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TimeHeapQueue(HeapQueue):
    now = staticmethod(time.time)

    def extendTime(self, time, items):
        """Time in units of now()'s return value.  Seconds is the unit for the default time.time()"""
        if time < self.now():
            return False
        append = self.append
        for item in items:
            append(time, item)
        return True
    def addTime(self, time, item):
        """Time in units of now()'s return value.  Seconds is the unit for the default time.time()"""
        if time < self.now():
            return False
        self.append(time, item)
        return True

    def extendDelta(self, delta, items):
        """Delta time in units of now()'s return value.  Seconds is the unit for the default time.time()"""
        if delta < 0:
            return False;

        append = self.append
        time = self.now() + delta
        for item in items:
            append(time, item)
        return True
    def addDelta(self, delta, item):
        """Delta time in units of now()'s return value.  Seconds is the unit for the default time.time()"""
        if delta < 0:
            return False
        self.append(self.now() + delta, item)
        return True

    def process(self, time=None):
        now = self.now()
        items = self.popItems(now)
        return now, items

    def popItems(self, time=None):
        return list(self.iterPopItems(time))

    def iterPopItems(self, time=None):
        if time is None:
            time = self.now()
        return HeapQueue.iterPopItems(self, time)

    def nextTime(self):
        return self.nextIndex()
    def nextDelta(self, minValue=None):
        next = self.nextIndex()
        if next is None:
            return next
        return max(minValue, next - self.now())


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    import sys
    import weakref

    class Expiry(object):
        name = None
        def __init__(self, name):
            self.name = name
        def __repr__(self):
            return '<%s %r>'%(self.__class__.__name__, self.name)
        def __del__(self):
            print "%r.__del__()" % (self,)

    thq = TimeHeapQueue()
    for t in xrange(10):
        thq.addDelta(t, Expiry(t))


    while thq:
        time.sleep(thq.nextDelta(0))

        now, items = thq.process()
        if items:
            print now, len(items), thq.nextDelta()
        else:
            print '\r%.3f' % (thq.nextDelta(), ),
            sys.stdout.flush()

