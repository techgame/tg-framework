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

from xml.sax.saxutils import quoteattr as _xmlquoteattr

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class xmlprefix(str):
    """A class change to distinguish xml prefixes from a namespace"""

def isXMLPrefix(obj):
    return isinstance(obj, xmlprefix)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class XMLNamespaceMap(object):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    default_xmlnsmap = {}

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Special Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __init__(self, nextmap=None, default_xmlnsmap=None):
        self.nextmap = nextmap
        if default_xmlnsmap: self.xmlnsmap = default_xmlnsmap
        else: self.xmlnsmap = self.default_xmlnsmap.copy()

    def __iter__(self):
        return self.iterxmlns(False)

    def __contains__(self, key):
        return key in self.xmlnsmap

    def __len__(self):
        return len(self.xmlnsmap)

    def __getitem__(self, key):
        return self.xmlnsmap[key]

    def __setitem__(self, key, value):
        raise NotImplementedError, "Use setxmlns instead."

    def __delitem__(self, key):
        del self.xmlnsmap[self.xmlnsmap[key]]
        del self.xmlnsmap[key]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def next(self):
        return self.nextmap

    def copy(self, klass=None):
        klass = klass or self.__class__
        return klass(self.next(), default_xmlnsmap=self.xmlnsmap.copy()) 

    def newChain(self, chainlevel=0, klass=None):
        klass = klass or self.__class__
        if chainlevel == 0:
            return klass(self) 
        elif chainlevel < 0 and self.next():
            return self.next().newChain(chainlevel+1, klass)
        else:
            return klass()

    def get(self, key, default=None):
        return self.xmlnsmap.get(key, default)

    def setxmlns(self, prefix, xmlns):
        """Adds an xml namespace mapping entry"""
        prefix = xmlprefix(prefix or '')
        try:
            key = self.xmlnsmap[prefix]
            del self.xmlnsmap[key]
        except KeyError: pass
        try:
            key = self.xmlnsmap[xmlns]
            del self.xmlnsmap[key]
        except KeyError: pass
        self.xmlnsmap[prefix] = xmlns
        self.xmlnsmap[xmlns] = prefix

    def _xmlns(self, prefix):
        return self.xmlnsmap[prefix]

    def xmlns(self, prefix, include_next=True):
        """Returns the xmlns string, given the prefix string"""
        try:
            return self._xmlns(prefix)
        except KeyError:
            if include_next and self.next() is not None:
                return self.next().xmlns(prefix)
            else: 
                return None

    def _prefix(self, xmlns):
        return str(self.xmlnsmap[xmlns])

    def prefix(self, xmlns, include_next=True):
        """Returns the prefix string, given the xmlns"""
        try:
            return self._prefix(xmlns)
        except KeyError:
            if include_next and self.next() is not None:
                return self.next().xmlns(xmlns)
            else: 
                return None

    def iterPrefix(self, include_next=True):
        for key, prefix in self.xmlnsmap.iteritems():
            if not isXMLPrefix(key): 
                yield prefix, key

        for prefix, ns in include_next and self.next() or ():
            if prefix not in self.xmlnsmap:
                yield prefix, ns

    def iterxmlns(self, include_next=True):
        for key, prefix in self.xmlnsmap.iteritems():
            if not isXMLPrefix(key): 
                yield key, prefix

        for prefix, ns in include_next and self.next() or ():
            if prefix not in self.xmlnsmap:
                yield ns, prefix

    def toXML(self, include_next=False):
        result = ['']
        for prefix, xmlns in self.iterPrefix(include_next):
            xmlns = _xmlquoteattr(xmlns or '')
            if prefix: result.append('xmlns:%s=%s' % (prefix, xmlns))
            else: result.append('xmlns=%s' % (xmlns,))
        return ' '.join(result)

