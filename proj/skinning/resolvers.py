#!/usr/bin/env python
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

import os
from TG.uriResolver import URI

from TG.uriResolver.utils import URIResolverRegistry

import TG.uriResolver.fileobj
import TG.uriResolver.utils

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SkinURIResolverRegistry(URIResolverRegistry):
    filenameKey = 'filename'
    skinKey = 'skin'

    def fromDefault(klass, uriBase='/', pathBase=os.getcwd()):
        result = klass()
        result.setupDefault(uriBase, pathBase)
        return result
    fromDefault = classmethod(fromDefault)

    def install(self):
        global registry
        registry = self

    def setupDefault(self, uriBase='/', pathBase=os.getcwd()):
        skinResolver = TG.uriResolver.fileobj.FileResolver(uriBase, pathBase)
        self[self.skinKey] = skinResolver
        self.setupFilenameResolver(uriBase, pathBase)

    def setupFilenameResolver(self, uriBase='/', pathBase=os.getcwd()):
        filenameResolver = TG.uriResolver.utils.FilenameURIResolver(uriBase, pathBase)
        filenameResolver.setHostResolver(self[self.skinKey])
        self[self.filenameKey] = filenameResolver

    def resolveFilename(self, filename, **kw):
        return self.get(self.filenameKey).resolve(filename, **kw)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ skinResolvers global
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

registry = SkinURIResolverRegistry.fromDefault()

