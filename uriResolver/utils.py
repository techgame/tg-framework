
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
from TG.uriResolver import base

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class URIResolverRegistry(dict):
    def __getattr__(self, keyname):
        if keyname in self:
            return self[keyname]
        else:
            dict.__getattr__(self, keyname)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class FilenameURIResolver(base.URIResolverBase):
    """Resolves a filename relative to pathBase into a URI relative to uri.

    Origionally written to resolve a module's __file__ attributes into a
    URINode from the host.  However, this method should work for any file under
    the pathBase.
    """

    def __init__(self, uri='/', pathBase=os.getcwd()):
        base.URIResolverBase.__init__(self, uri)
        self.setURIRootFromPath(pathBase)

    def getURIRoot(self):
        return self.uriRoot
    def setURIRoot(self, uriRoot):
        self.uriRoot = uriRoot
    def setURIRootFromPath(self, path):
        uri = self.asFileURI(path)
        self.setURIRoot(uri)

    def _visitURI(self, uriRaw, relative=True):
        uri = self.asFileURI(uriRaw)
        uri = self.uriRoot.asSubpath(uri, True)

        uriBase = self.getURI()
        if relative and uriBase is not None:
            uri = uriBase.join(uri)
        return uri, uri

    def asFileURI(self, filename, simplify=True):
        if not isinstance(filename, basestring):
            filename = unicode(filename)
        filename = os.path.abspath(filename)
        filename = filename.replace(os.sep, '/')
        uriFile = URI('file:'+filename)
        if simplify:
            del uriFile.scheme
            del uriFile.authority
        return uriFile

