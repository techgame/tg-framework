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

try: 
    set
except NameError:
    from sets import Set as set

from copy import copy as _copy

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ SinkCollections
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SinkCollectionBase(object):
    _data = None
    _dataFactory = None

    def getData(self):
        if self._data is None:
            self._data = self._dataFactory()
        return self._data
    def setData(self, data):
        self._data = data
    data = property(getData, setData)

    def __copy__(self):
        result = self.__class__()
        result.setData(_copy(self.getData()))
        return result

    def __deepcopy__(self, memo):
        return _copy(self)

    def __nonzero__(self):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def __iter__(self):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

    def add(self, sink):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def remove(self, sink):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def clear(self):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Sink Collections Implementations
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SinkListCollection(SinkCollectionBase):
    _dataFactory = list

    def __nonzero__(self):
        return bool(self.data)

    def add(self, sink):
        self.data.append(sink)
        return sink

    def remove(self, sink):
        self.data.remove(sink)
        return sink

    def clear(self, sink):
        del self.data[:]

    def __iter__(self):
        return iter(self.data)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SinkSetCollection(SinkCollectionBase):
    _dataFactory = set

    def __nonzero__(self):
        return bool(self.data)

    def add(self, sink):
        self.data.add(sink)
        return sink

    def remove(self, sink):
        self.data.remove(sink)
        return sink

    def clear(self):
        self.data.clear()

    def __iter__(self):
        return iter(self.data)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ NotificationBase Mixins
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class PlugableSinkCollection(object):
    """For mixing in with Notification class"""
    SinkCollectionFactory = SinkListCollection
    _sinks = None

    def __nonzero__(self):
        return bool(self.getSinks())

    def getSinks(self):
        """Returns an instance implementing SinkCollection"""
        if self._sinks is None:
            self.createSinkCollection()
        return self._sinks
    def setSinks(self, sinks):
        """Sets an instance implementing Sinks"""
        self._sinks = sinks
    sinks = property(getSinks, setSinks)

    def iterSinks(self):
        return iter(self.getSinks())

    def createSinkCollection(self):
        sinkCollection = self.SinkCollectionFactory()
        self.setSinks(sinkCollection)
        return sinkCollection

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class PlugableSinkCollectionExtended(PlugableSinkCollection):
    #~ Sink Collection Delegation ~~~~~~~~~~~~~~~~~~~~~~~

    def add(self, sink):
        return self.getSinks().add(sink)
    def remove(self, sink):
        return self.getSinks().remove(sink)
    def clear(self):
        return self.getSinks().clear()

    def addSink(self, sink):
        return self.add(sink)
    def removeSink(self, sink):
        """LookupError safe version of remove"""
        try: 
            return self.remove(sink)
        except LookupError:
            pass
    def clearSinks(self):
        self.clear()

