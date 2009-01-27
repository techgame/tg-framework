
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

## stdlib:
try: 
    import cStringIO as StringIO
except ImportError:
    import StringIO

## TG:
from TG.uriResolver import URI
import filebase

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class GenericContainer(object):
    DataFileFactory = StringIO.StringIO

    def filePath(self, fileNode):
        return fileNode.getPath()

    def fileExists(self, fileNode):
        return fileNode.getData() is not None

    def fileOpen(self, fileNode, *args, **kw):
        data = fileNode.getData()
        if data is None:
            raise ValueError("Generic data does not exist for node %r!" % fileNode)
        return self.DataFileFactory(data)

    def pathJoin(self, *parts):
        return '/'.join(parts)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class GenericNodeBase(filebase.FileNodeBase):
    pass

class GenericNode(GenericNodeBase):
    def getData(self):
        return self.data
    def setData(self, data):
        self.data = data

    def getPath(self):
        return self.path
    def setPath(self, path):
        self.path = path

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class GenericResolver(filebase.FileResolverEx):
    NodeFactory = GenericNode
    FileContainerFactory = GenericContainer

    def createNodeForURI(self, uri, uriContained, path):
        node = filebase.FileResolverEx.createNodeForURI(self, uri, uriContained, path)
        self.setNodeData(node)
        return node

    def setNodeData(self, node):
        # node.setData(self.datadict.get(path, None)
        raise NotImplementedError('Subclass Responsibility')

