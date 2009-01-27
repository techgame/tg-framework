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

import new
from threading import Thread

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def dispatch(table, key):
    """Decorator that sets 'table[key] = method'"""
    def addDispatchEntry(method):
        table[key] = method
        return method
    return addDispatchEntry

def threadcall(method):
    def decorate(*args, **kw):
        t = Thread(target=method, args=args, kwargs=kw)
        t.setDaemon(True)
        t.start()
        return t
    decorate.__name__ = method.__name__
    decorate.__doc__ = method.__doc__
    return decorate

def threadcallExclusive(method):
    def decorate(*args, **kw):
        if decorate.thread and decorate.thread.isAlive():
            return decorate.thread
        t = Thread(target=method, args=args, kwargs=kw)
        t.setDaemon(True)
        t.start()
        decorate.thread = t
        return t
    decorate.thread = None
    decorate.__name__ = method.__name__
    decorate.__doc__ = method.__doc__
    return decorate

class nsmethod(object):
    def __init__(self, function):
        self.function = function

    instancemethod = staticmethod(new.instancemethod)
    def __get__(self, instance, instanceKlass):
        if instance is None:
            instance = instanceKlass
        return self.instancemethod(self.function, instance, instanceKlass)

