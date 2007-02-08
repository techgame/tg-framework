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
import os
import types

from TG.introspection.code import compileWithFileAndLine

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class DynamicModule(types.ModuleType):
    @classmethod
    def getModuleName(klass, __file__):
        return 'dynamic:%s' % (klass.__name__,)

    @classmethod
    def fromFilename(klass, __file__, **kw):
        source = open(__file__, 'r').read()
        return klass.fromSource(source, __file__, **kw)

    @classmethod
    def fromSource(klass, __source__, __file__, **kw):
        self = klass(klass.getModuleName(__file__))
        self.__file__ = __file__

        source = open(__file__, 'r').read()
        code = self.compileWithFileAndLine(source, 'exec', __file__, 1)
        return self.execSrc(code, kw)

    compileWithFileAndLine = staticmethod(compileWithFileAndLine)

    def execSrc(self, code, locals):
        self.__dict__.update(locals)

        dirpath = os.path.dirname(self.__file__)
        sys.path.insert(0, dirpath)
        try:
            exec code in self.__dict__
        finally:
            sys.path.remove(dirpath)
        return self

