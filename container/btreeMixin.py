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

class BTreeDictMixin(object):
    _sentinal = object()

    def __init__(self, dict=None, **kw):
        super(BTreeDictMixin, self).__init__()
        if dict: 
            self.update(dict)
        if kw: 
            self.update(kw)

    def __cmp__(self, other):
        raise NotImplementedError("TODO")

    def copy(self):
        raise NotImplementedError("TODO")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __nonzero__(self):
        return bool(self._getRootNode())

    def __iter__(self):
        return self.iterkeys()

    def items(self):
        return list(self.iteritems())
    def iteritems(self):
        return self._getRootNode().iteritems()

    def keys(self):
        return list(self.iterkeys())
    def iterkeys(self):
        return (k for k,v in self.iteritems())

    def values(self):
        return list(self.itervalues())
    def itervalues(self):
        return (v for k,v in self.iteritems())

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __contains__(self, key):
        return self.has_key(key)
    def has_key(self, key):
        return self._find(key, self._sentinal) is not self._sentinal

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __getitem__(self, key):
        return self._find(key)[1]
    def __setitem__(self, key, value):
        self._insert(key, value)
    def __delitem__(self, key):
        self._delete(key)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def clear(self):
        self._newRootNode()

    def get(self, key, default=None):
        return self._find(key, default)
    def pop(self, key, *args):
        return self._pop(key, *args)
    def popitem(self):
        node = self._getRootNode()
        if node:
            key = node.getItems()[0][0]
            return (key, self._pop(key))
        else:
            raise KeyError("BTree is empty")

    def setdefault(self, key, default=None):
        result = self.get(key, self._sentinal)
        if result is self._sentinal:
            self[key] = default
            return default
        else:
            return result

    def update(self, other=None, **kwargs):
        # Make progressively weaker assumptions about "other"
        if other is None:
            pass
        elif hasattr(other, 'iteritems'):  # iteritems saves memory and lookups
            for k, v in other.iteritems():
                self[k] = v
        elif hasattr(other, 'keys'):
            for k in other.keys():
                self[k] = other[k]
        else:
            for k, v in other:
                self[k] = v

        if kwargs:
            for k, v in kwargs.iteritems():
                self[k] = v

