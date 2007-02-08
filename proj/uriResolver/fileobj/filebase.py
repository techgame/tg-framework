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

from TG.uriResolver.base import URI, URIResolutionError
from TG.uriResolver.base import URIResolverBase
from TG.uriResolver.node import URINodeBase
from TG.uriResolver.node import NodeCacheingBaseMixin

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ File Containers and Contained
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class FileContainerAbstract(object):
    def filePath(self, fileNode):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def fileExists(self, fileNode):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def fileOpen(self, fileNode, *args, **kw):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def pathJoin(self, *parts):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

#~ File Container User Mixin ~~~~~~~~~~~~~~~~~~~~~~~~

class FileContainerMixin(object):
    _fileContainer = None
    FileContainerFactory = FileContainerAbstract

    #~ FileContainer API ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getFileContainer(self):
        if self._fileContainer is None:
            self.createFileContainer()
        return self._fileContainer
    def setFileContainer(self, fileContainer):
        self._fileContainer = fileContainer
    fileContainer = property(getFileContainer, setFileContainer)

    def createFileContainer(self):
        container = self.FileContainerFactory()
        self.setFileContainer(container)

#~ Contained Node Mixin ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ContainedNodeMixin(object):
    _fileContainer = None

    def getFileContainer(self):
        return self._fileContainer
    def setFileContainer(self, fileContainer):
        self._fileContainer = fileContainer
    fileContainer = property(getFileContainer, setFileContainer)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ File Node 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class FileNodeAbstract(URINodeBase):
    #~ File Node API ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getPath(self, fileNode):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def exists(self):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def open(self, *args, **kw):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class FileNodeBase(URINodeBase, ContainedNodeMixin):
    _path = None

    def __init__(self, uri, path):
        URINodeBase.__init__(self, uri)
        self.setSubPath(path)

    def __repr__(self):
        return "<%s.%s \"%s\">" % ( self.__class__.__module__, self.__class__.__name__, self.getSubPath())

    #~ File Node API ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getPath(self):
        return self.getFileContainer().filePath(self)

    def exists(self):
        return self.getFileContainer().fileExists(self)

    def open(self, *args, **kw):
        return self.getFileContainer().fileOpen(self, *args, **kw)

    #~ File Node Path APIs ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getSubPath(self):
        return self._subpath
    def setSubPath(self, subpath):
        self._subpath = subpath

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ File Resolvers
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class URIDoesNotExistError(URIResolutionError):
    errFmt = "Could not resolve %r on %r: Does not exist!"

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class FileResolverBase(URIResolverBase):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    _uri = URI('')
    _path = None
    URIDoesNotExistError = URIDoesNotExistError

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __init__(self, uri=None, path=_path):
        URIResolverBase.__init__(self, uri)
        self.setPath(path)

    #~ Path Property ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getPath(self):
        return self._path
    def setPath(self, path):
        self._path = path

    #~ URI Resolver API ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def containsExtended(self, uriFull, uriRemnant):
        # Even if the file does not exist, we "contain" it so that errors
        # can be intelligable
        uriContained = self.asContainedURI(uriFull, uriRemnant)
        return uriContained is not None

    def resolveExtended(self, uriFull, uriRemnant, **kw):
        uriContained = self.asContainedURI(uriFull, uriRemnant)
        if uriContained is not None:
            node = self.resolveToNode(uriFull, uriContained, **kw)
            if node is None:
                self.unresolvedNode(uriFull, uriContained, node)
            return node
        else:
            return self.resolveFromHost(uriFull, **kw)

    def unresolvedNode(self, uri, uriContained, node):
        raise self.URIDoesNotExistError(uri, self)

    #~ FileReolver API ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def resolveToNode(self, uri, uriContained, **kw):
        raise NotImplementedError('Subclass Responsibility')

    def asContainedURI(self, uriFull, uriRemnant):
        """Override to implement constraining semantics.  Return contained URI or None."""
        uri = self.getURI()
        if uri.isRelative(uriRemnant, True, False):
            # we are in the same scheme
            if uriRemnant.isAbsPath():
                # ok, see if the subpaths match
                result = uri.asSubpath(uriRemnant, True)
            else:
                # assume we have a match since it's relative
                result = uriRemnant
        elif uri.isRelative(uriFull, True, False):
            # we are in the same scheme, so the result is determined by whether this item's subpath matches
            result = uri.asSubpath(uriFull, True)
        else:
            # nope.  lets get outa here
            result = None

        return result

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class FileResolverBaseEx(FileResolverBase, FileContainerMixin):
    def _getContainedPath(self, uri):
        """Override to implement additional semantics.  Return contained URI or None."""
        return self.getFileContainer().pathJoin(*uri.getPathEx())

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class FileResolverEx(NodeCacheingBaseMixin, FileResolverBaseEx):
    NodeFactory = FileNodeBase
    FileContainerFactory = FileContainerAbstract

    def resolveToNode(self, uri, uriContained, **kw):
        path = self._getContainedPath(uriContained)
        node = self._getCachedNode(path)
        if node is None:
            node = self.createNodeForURI(uri, uriContained, path)

            if not node.exists():
                if kw.get('mustExist', True):
                    node = None

        if node is not None:
            self._addCahcedNode(path, node)
        return node

    def createNodeForURI(self, uri, uriContained, path):
        node = self.NodeFactory(uri, path)
        node.setHostResolver(self)
        node.setFileContainer(self.getFileContainer())
        return node

