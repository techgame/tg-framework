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

import base
import weakref

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Node and Node Caching
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class URINodeBase(base.URIResolverBase):
    pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Node Cacheing for Resolvers
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class NodeCacheingBaseMixin(object):
    def _getCachedNode(self, key):
        return None

    def _addCahcedNode(self, key, node):
        pass

class NodeCacheingMixin(NodeCacheingBaseMixin):
    #~ Node Cacheing ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    NodeCacheFactory = weakref.WeakValueDictionary
    _nodeCache = None

    def _getCachedNode(self, key):
        if self._nodeCache is not None:
            return self._nodeCache.get(key, None)
        else:
            return None

    def _addCahcedNode(self, key, node):
        if self._nodeCache is None:
            self._nodeCache = {}
        self._nodeCache[key] = node

