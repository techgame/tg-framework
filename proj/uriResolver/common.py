##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##~ Copyright (C) 2002-2004  TechGame Networks, LLC.
##~ 
##~ This library is free software; you can redistribute it and/or
##~ modify it under the terms of the BSD style License as found in the 
##~ LICENSE file included with this distribution.
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = """
    AuthorityResolver
    PathResolver
    SchemeAuthorityResolver
    SchemeResolver
    """.split()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import base
from base import URI

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ URI Composite Resolvers
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class URICompositeResolver(base.URICompositeResolverBase):
    _resolvers = None
    ResolverFactory = list

    def getResolvers(self):
        if self._resolvers is None:
            self.setResolvers(self.ResolverFactory())
        return self._resolvers
    def setResolvers(self, resolvers):
        self._resolvers = resolvers
    resolvers = property(getResolvers, setResolvers)

    def iterResolvers(self):
        return iter(self.getResolvers())

    #~ URI Resolver API ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def iterResolversForURI(self, uriFull, uriRemnant):
        for resolver in self.iterResolvers():
            if resolver.containsExtended(uriFull, uriRemnant):
                yield uriRemnant, resolver

#~ Dict based: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class URIKeyedCompositeResolver(URICompositeResolver):
    ResolverFactory = dict

    #~ URI Resolver API ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def iterResolvers(self):
        return self.getResolvers().iteritems()

    def iterResolversForURI(self, uriFull, uriRemnant):
        uriSub, key = self._keyFromURI(uriFull, uriRemnant)
        if uriSub is not None: 
            delegate = self.getResolverForKey(key)
            if delegate is not None:
                yield uriSub, delegate

        result = self.getResolverDefault(uriFull, uriRemnant)
        if result:
            yield result

    def getResolverDefault(self, uriFull, uriRemnant):
        return None

    def getResolverForKey(self, key):
        return self.getResolvers().get(key, None)

    #~ Add/Remove Resolvers ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def addResolverForKey(self, resolver, key):
        resolvers = self.getResolvers()
        resolvers[key] = resolver
    def removeResolverForKey(self, key):
        resolvers = self.getResolvers()
        if key in resolvers:
            del resolvers[key]

    def addDefaultResolver(self, resolver):
        self.addResolverForKey(resolver, self._keyDefault())
    def removeDefaultResolver(self, resolver):
        self.removeResolverForKey(self._keyDefault())

    def addResolverForURI(self, resolver, uriRaw, relative=False):
        uriFull, uriRemnant = self._visitURI(uriRaw, relative)
        uriSub, key = self._keyFromURI(uriFull, uriRemnant)
        self.addResolverForKey(resolver, key)
    def removeResolverForURI(self, uriRaw, relative=False):
        uriFull, uriRemnant = self._visitURI(uriRaw, relative)
        uriSub, key = self._keyFromURI(uriFull, uriRemnant)
        self.removeResolverForKey(key)

    #~ subclass API ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _keyFromURI(self, uriFull, uriRemnant):
        raise NotImplementedError('Subclass Responsibility')

    def _keyDefault(self):
        return None

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Usable Resolvers
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SchemeResolver(URIKeyedCompositeResolver):
    defaultScheme = None

    def _keyFromURI(self, uriFull, uriRemnant):
        scheme = uriRemnant.scheme
        if scheme is None:
            scheme = self.defaultScheme
        else:
            del uriRemnant.scheme
        return uriRemnant, scheme

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class AuthorityResolver(URIKeyedCompositeResolver):
    defaultAuthority = None

    def _keyFromURI(self, uriFull, uriRemnant):
        authority = uriFull.authority
        if authority is None:
            authority = self.defaultAuthority
        return uriRemnant, authority

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SchemeAuthorityResolver(URIKeyedCompositeResolver):
    defaultScheme = None
    defaultAuthority = None

    def _keyFromURI(self, uriFull, uriRemnant):
        scheme, authority = uriFull.scheme, uriFull.authority
        if scheme is None:
            scheme = self.defaultScheme
        if authority is None:
            authority = self.defaultAuthority
        return uriRemnant, (scheme, authority)

    def _keyDefault(self):
        return (self.defaultScheme, self.defaultAuthority)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class PathResolver(URIKeyedCompositeResolver):
    _uri = URI('/')

    def _keyFromURI(self, uriFull, uriRemnant):
        uri = uriRemnant
        if uriRemnant is not None:
            uriSubpath = uri.fromURI(uriRemnant, True)
            path = uriRemnant.getPathEx().normalized()
            uriSubpath.setPathEx(path[1:])
            key = (path and path[0]) or self._keyDefault()
            return uriSubpath, key
        else:
            return None, None
    
    def mount(self, resolver, uriRelative=None):
        if uriRelative is None:
            uriRelative = resolver.getURIPart()
        return self.addResolverForURI(resolver, uriRelative, True)
    def unmount(self, uriRelative):
        return self.removeResolverForURI(uriRelative, True)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def containsLocal(self, uriFull, uriRemnant, **kw):
        # define the 'current directory'
        return (uriRemnant == "") 

    def resolveLocal(self, uriFull, uriRemnant, **kw):
        if uriRemnant == "":
            return self
        else:
            return URIKeyedCompositeResolver.resolveLocal(self, uriFull, uriRemnant, **kw)

