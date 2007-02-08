##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##~ Copyright (C) 2002-2004  TechGame Networks, LLC.
##~ 
##~ This library is free software; you can redistribute it and/or
##~ modify it under the terms of the BSD style License as found in the 
##~ LICENSE file included with this distribution.
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = """
    URI
    ZipContainer
    ZipNode
    ZipResolver
    """.split()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os
import zipfile
import re

try: 
    import cStringIO as StringIO
except ImportError:
    import StringIO

from TG.uriResolver import base, node, URI
from TG.uriResolver.node import NodeCacheingMixin

import filebase

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ZipContainer(zipfile.ZipFile):
    StringIOFactory = StringIO.StringIO

    def filePath(self, fileNode):
        return os.path.join(self.filename, fileNode.getSubPath())

    def fileExists(self, fileNode):
        filename = self._getZipName(fileNode)
        return filename in self.namelist()

    def fileOpen(self, fileNode, *args, **kw):
        filename = self._getZipName(fileNode)
        return self.StringIOFactory(self.read(filename))

    def _getZipName(self, fileNode):
        return fileNode.getSubPath()

    def pathJoin(self, *parts):
        return '/'.join(parts)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ZipNode(filebase.FileNodeBase):
    pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ZipResolver(NodeCacheingMixin, filebase.FileResolverEx):
    NodeFactory = ZipNode
    FileContainerFactory = ZipContainer

    def createFileContainer(self):
        container = self.FileContainerFactory(self.getPath())
        self.setFileContainer(container)

