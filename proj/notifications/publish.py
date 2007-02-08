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

import engine

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Publisher(engine.PlugableNotification):
    """Makes publish() the notify interface"""
    def publish(self, *args, **kw):
        return self._notify(*args, **kw)

PublisherProperty = Publisher.property

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class DataPublisher(Publisher):
    """Makes set() an alternative notify interface"""

    data = None
    def __init__(self, data=None, *args, **kw):
        if data is not None:
            self.set(data)
        Publisher.__init__(self, *args, **kw)

    def get(self):
        return self.data

    def set(self, data, *args, **kw):
        self.data = data
        self.publish(self.data, *args, **kw)

    def update(self, *args, **kw):
        self.publish(self.data, *args, **kw)

    def callAndAdd(self, sink):
        result = self.add(sink)
        sink(self.get())
        return result

DataPublisherProperty = DataPublisher.property
DataPublisherObjectProperty = DataPublisher.objProperty

