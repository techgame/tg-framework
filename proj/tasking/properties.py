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

import copy
from TG.common.properties import DecoLazyProperty, PropertyFactory

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TaskListProperty(DecoLazyProperty):
    _cacheNamePrefix = '__tasklist_%s'

    _hostInitMethod = None
    def setInitMethod(self, method):
        self._hostInitMethod = method
        return method

    def onCreate(self, propObj, hostObj):
        DecoLazyProperty.onCreate(self, propObj, hostObj)

        if self._hostInitMethod:
            initMethod = getattr(hostObj, self._hostInitMethod.__name__, self._hostInitMethod)
            if initMethod:
                initMethod(propObj)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Decorator support for Notification 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def add(self, method, *args, **kw):
        return self._addDecorated('add', method, *args, **kw)

    def remove(self, method):
        return self._removeDecoratedByHostMethod(method)

    def setIdle(self, method):
        return self._addDecorated('setIdleTask', method, *args, **kw)
    def addDelegate(self, method, methodIsReady=lambda: True):
        return self._addDecorated('addDelegate', method, *args, **kw)

    def addCallMany(self, method, *args, **kw):
        return self._addDecorated('addCallMany', method, *args, **kw)

    def addCallOnce(self, method, *args, **kw):
        return self._addDecorated('addCallOnce', method, *args, **kw)

    def addIter(self, method, *args, **kw):
        return self._addDecorated('addIter', method, *args, **kw)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TaskListPropertyFactory(PropertyFactory):
    PropertyClass = TaskListProperty

