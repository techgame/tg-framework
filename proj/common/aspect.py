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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class BranchableObject(object):
    __rootClass = None

    def isBranchedClass(klass):
        return klass.__rootClass is not None
    isBranchedClass = classmethod(isBranchedClass)
    def _getRootClass(klass):
        return klass.__rootClass or klass
    _getRootClass = classmethod(_getRootClass)
    def _setRootClass(klass, rootClass):
        klass.__rootClass = rootClass
    _setRootClass = classmethod(_setRootClass)

    def _branchClass(klass, klassDict=None, **kwKlassDict):
        rootClass = klass._getRootClass()
        if klassDict: kwKlassDict.update(klassDict)
        kwKlassDict.update(__module__=klass.__module__)
        result = type(rootClass.__name__, (rootClass,), kwKlassDict)
        assert klass.__module__ == result.__module__
        result._setRootClass(rootClass)
        return result
    _branchClass = classmethod(_branchClass)

