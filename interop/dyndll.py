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
import ctypes
import ctypes.util

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MissingAPIException(Exception):
    _name = None
    def __init__(self, name, *args, **kw):
        self._name = name
        Exception.__init__(self, name, *args, **kw)
    def __repr__(self):
        return "<<%s: %r>>" % (self.__class__.__name__, self._name)
    def __nonzero__(self):
        return False
    def __call__(self, *args, **kw):
        raise self # They called the missing method, so raise an error

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def getAPIFunc(self, funcName):
    try:
        result = self._entryPointFuncPtr(funcName, self)
    except AttributeError:
        return None
    else:
        result.__name__ = funcName
        return result

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class APIDecorator(object):
    _name = None
    _handle = 0 # set from host in __init__
    _entryPointFuncPtr = None # set from host in __init__
    MissingAPIException = MissingAPIException

    def __init__(self, host, defaultErrCheck=None):
        self._name = host._name
        self._handle = host._handle
        self._entryPointFuncPtr = host._entryPointFuncPtr

        if defaultErrCheck is not None:
            self.defaultErrCheck = defaultErrCheck

    def __call__(self, restype, params, errcheck=NotImplemented):
        return self.decl(restype, params, errcheck)
    def decl(self, restype, params, errcheck=NotImplemented):
        def decorate(func):
            api = self._getAPIFuncFromPyFunc(func)
            if api is not None:
                return self._declFoundAPI(func, api, restype, params, errcheck)
            else:
                return self._declMissingAPI(func, api, restype, params, errcheck)

        return decorate

    getAPIFunc = getAPIFunc
    def _getAPIFuncFromPyFunc(self, func):
        return self.getAPIFunc(func.__name__)

    def _declFoundAPI(self, func, api, restype, params, errcheck=NotImplemented):
        if errcheck is NotImplemented:
            errcheck = self.defaultErrCheck

        api.restype = restype
        api.argtypes = tuple(params)
        if errcheck is not None:
            api.errcheck = errcheck
        func._api_ = api
        return func

    def _declMissingAPI(self, func, api, restype, params, errcheck=NotImplemented):
        func._api_ = self.MissingAPIException(func.__name__)
        return func

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class DynamicLibrary(object):
    _name = None
    _handle = 0
    _mode = ctypes.RTLD_LOCAL
    APIDecoratorFactory = APIDecorator

    class DynamicFuncPtr(ctypes._CFuncPtr):
        _flags_ = ctypes._FUNCFLAG_CDECL
        _restype_ = ctypes.c_int # default, can be overridden in instances

        def __init__(self, name, host):
            self._name = self.__name__ = name
            self._hostname = host._name
            ctypes._CFuncPtr.__init__(self, name, host)

        def __repr__(self):
            return '<%s %s.%s>' % (self.__class__.__name__, self._hostname, self._name)
    _entryPointFuncPtr = DynamicFuncPtr

    def __init__(self, name=None, handle=0, mode=None):
        self._loadLibrary(name, handle, mode)

    def _loadLibrary(self, name=None, handle=0, mode=None):
        self._name = name or self._name
        self._handle = handle or self._handle
        self._mode = mode or self._mode

        if not self._handle:
            self._handle = ctypes._dlopen(self._name, self._mode)

    def __repr__(self):
        return "<%s '%s', handle %x at %x>" % (self.__class__.__name__, self._name, (self._handle & (sys.maxint*2 + 1)), id(self))

    getAPIFunc = getAPIFunc

    def apiType(self, defaultErrCheck=None):
        return self.APIDecoratorFactory(self, defaultErrCheck)

    def addAPIType(self, name):
        def decorate(errorFunc):
            newAPIType = self.apiType(errorFunc)
            setattr(self, name, newAPIType)
            return errorFunc
        return decorate


dynLibs = ctypes.LibraryLoader(DynamicLibrary)

