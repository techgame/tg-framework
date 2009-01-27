##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##~ Copyright (C) 2002-2004  TechGame Networks, LLC.
##~ 
##~ This library is free software; you can redistribute it and/or
##~ modify it under the terms of the BSD style License as found in the 
##~ LICENSE file included with this distribution.
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = """
    URI
    FilesystemContainer
    FileNode
    FileResolver
    """.split()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os

from TG.uriResolver import URI
from TG.uriResolver.node import NodeCacheingMixin

import filebase

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ File Resolver 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class FilesystemContainer(filebase.FileContainerAbstract):
    def filePath(self, fileNode):
        return fileNode.getPath()

    def fileExists(self, fileNode):
        filename = self.filePath(fileNode)
        return os.path.exists(filename)

    def fileOpen(self, fileNode, *args, **kw):
        filename = self.filePath(fileNode)
        return file(filename, *args, **kw)

    def pathJoin(self, *parts):
        return os.path.join(*parts)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class FileNode(filebase.FileNodeBase):
    _basePath = None

    def getBasePath(self):
        return self._basePath
    def setBasePath(self, basePath):
        self._basePath = basePath
    basePath = property(getBasePath, setBasePath)

    def getPath(self):
        return self.getFileContainer().pathJoin(self.getBasePath(), self.getSubPath())

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class FileResolver(NodeCacheingMixin, filebase.FileResolverEx):
    _uriBase = URI('./')
    _path = os.getcwd()

    NodeFactory = FileNode
    FileContainerFactory = FilesystemContainer

    #~ FileReolver API ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def createNodeForURI(self, uri, uriContained, path):
        node = filebase.FileResolverEx.createNodeForURI(self, uri, uriContained, path)
        node.setBasePath(self.getPath())
        return node

