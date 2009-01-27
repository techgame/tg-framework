#!/usr/bin/env python
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##~ Copyright (C) 2002-2004  TechGame Networks, LLC.
##~ 
##~ This library is free software; you can redistribute it and/or
##~ modify it under the terms of the BSD style License as found in the 
##~ LICENSE file included with this distribution.
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = """
    URI
    URIResolutionError   
    """.split()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from TG.w3c.uri import URI

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class URIResolutionError(Exception):
    errFmt = "Could not resolve %r on %r"

    def __init__(self, uri, resolver=None, messages='', errFmt=errFmt):
        self.uri = uri
        self.resolver = resolver
        self.messages = messages

    def __str__(self):
        result = self.errFmt % (self.uri, self.resolver)
        if self.messages:
            result += ': ' + self.messages
        return result

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class URIResolverAbstract(object):
    #~ URI Resolver API ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    URIResolutionError = URIResolutionError

    def contains(self, uriRaw):
        """Override .containsExtended instead"""
        uriFull, uriRemnant = self._visitURI(uriRaw)
        return self.containsExtended(uriFull, uriRemnant)

    def resolve(self, uriRaw, default=NotImplemented, **kw):
        """Override .resolveExtended instead"""
        uriFull, uriRemnant = self._visitURI(uriRaw)
        try:
            result = self.resolveExtended(uriFull, uriRemnant, **kw)
        except self.URIResolutionError, e:
            if default is NotImplemented:
                raise
            return default
        else:
            return result

    def containsExtended(self, uriFull, uriRemnant):
        raise NotImplementedError('Subclass Responsibility')

    def resolveExtended(self, uriFull, uriRemnant, **kw):
        raise NotImplementedError('Subclass Responsibility')

    def _visitURI(self, uriRaw, relative=True):
        raise NotImplementedError('Subclass Responsibility: %r' % (self.__class__,))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Resolvable URI
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class URIResolvable(URI, URIResolverAbstract):
    _resolver = None
    def __init__(self, uri, resolver, *args, **kw):
        URI.__init__(self, uri, *args, **kw)
        if resolver is None and hasattr(uri, 'getResolver'):
            resolver = uri.getResolver()
        self.setResolver(resolver)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def contains(self, uriRaw):
        if uriRaw == None: uriRaw = self
        return URIResolverAbstract.contains(self, uriRaw)

    def resolve(self, uriRaw=None, *args, **kw):
        if uriRaw == None: uriRaw = self
        return URIResolverAbstract.resolve(self, uriRaw, *args, **kw)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def asResolvableURI(self):
        return self

    def getResolver(self):
        return self._resolver
    def setResolver(self, resolver):
        self._resolver = resolver
    resolver = property(getResolver, setResolver)

    def containsExtended(self, uriFull, uriRemnant):
        return self.getResolver().containsExtended(uriFull, uriRemnant)
    def resolveExtended(self, uriFull, uriRemnant, **kw):
        return self.getResolver().resolveExtended(uriFull, uriRemnant, **kw)
    def _visitURI(self, uriRaw, relative=True):
        return self.getResolver()._visitURI(uriRaw, relative=True)

    #~ pickle persistence ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __getstate__(self):
        data = URI.__getstate__(self)
        data['_resolver'] = self._resolver
        return data
    def __setstate__(self, data):
        URI.__setstate__(self, data)
        self._resolver = self.data.pop('_resolver', None)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def copyFromURIParts(self, uriParts):
        result = self.__class__(None, self.getResolver())
        result.setURIParts(uriParts)
        return result

    def copyFromURI(self, uriOther):
        return self.__class__(uriOther, self.getResolver())

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ URI Resolver Base
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class URIResolverBase(URIResolverAbstract):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    _uri = None
    _uriPart = None
    _hostResolver = None
    URIResolvableFactory = URIResolvable

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __init__(self, uri=None, **kw):
        if uri is not None:
            self.setURI(uri)
        else:
            uriPart = kw.get('uriPart', None)
            if uriPart is not None:
                self.setURIPart(uriPart)

    def __repr__(self):
        return "<%s.%s for: %r>" % (
                self.__class__.__module__,
                self.__class__.__name__,
                self.getURI(False))

    def __getstate__(self):
        data = self.__dict__.copy()
        data.pop('_uri', None) # don't save the uri
        return data

    #~ Attributes ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getURI(self, updateIfAbsent=True):
        if self._uri is None and updateIfAbsent:
            self.updateURI()
        return self._uri
    def setURI(self, uri, regress=True):
        self._uri = URI(uri)
        if regress:
            self.onSetURI(uri)
    def onSetURI(self, uri):
        pass
    uri = property(getURI, setURI)

    def getURIPart(self):
        return self._uriPart
    def setURIPart(self, uriPart):
        self._uriPart = uriPart
        self.updateURI()
    uriPart = property(getURIPart, setURIPart)

    def updateURI(self):
        host = self.getHostResolver()
        uriPart = self.getURIPart()
        if host is not None and uriPart is not None:
            uriHost = host.getURI()
            uri = uriHost.append(uriPart)
            self.setURI(uri, False)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def asResolvableURI(self, uri=None, asRelativeTo=False):
        if uri is None:
            uri = self.getURI()
        elif asRelativeTo:
            uri = self.getURI().asRelativeTo(uri)
        return self.URIResolvableFactory(uri, self)

    #~ URI Resolver API ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getHostResolver(self):
        return self._hostResolver
    def setHostResolver(self, hostResolver, uri=NotImplemented):
        self._hostResolver = hostResolver
        if uri is not NotImplemented:
            self.setURI(uri)
    hostResolver = property(getHostResolver, setHostResolver)

    #~ URI Resolover Common Implementation ~~~~~~~~~~~~~~

    def __contains__(self, uri):
        return self.contains(uri)

    def resolveFromHost(self, uriFull, **kw):
        host = self.getHostResolver()
        if host:
            return host.resolveExtended(uriFull, uriFull, **kw)
        else:
            raise self.URIResolutionError(uriFull, self, 'Host resolver not set')

    #~ URI Resolver API ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def containsExtended(self, uriFull, uriRemnant):
        """Override with .containsExtended"""
        # Note: Override containsExtended and containsExtended to
        # implement subclass
        return False
    def resolveExtended(self, uriFull, uriRemnant, **kw):
        """Override with .resolveExtended"""
        # Note: Override resolveExtended and resolveExtended to
        # implement subclass
        return self.resolveFromHost(uriFull, **kw)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Protected Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _visitURI(self, uriRaw, relative=True):
        uri = URI(uriRaw)
        if relative:
            uriBase = self.getURI()
            if uriBase is not None:
                uriFull = uriBase.join(uri)
                uriRemnant = uriBase.asSubpath(uriFull, True)
                if uriRemnant is None:
                    uriRemnant = uriFull
                else:
                    uriRemnant.standardize()
                return uriFull, uriRemnant
        return uri, uri

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ URI Composite Resolver Base
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class URICompositeResolverBase(URIResolverBase):
    def onSetURI(self, uri):
        URIResolverBase.onSetURI(self, uri)
        for child in self.iterResolvers():
            child.updateURI()

    #~ URI Resolver API ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def resolveExtended(self, uriFull, uriRemnant, **kw):
        for subURI, resolver in self.iterResolversForURI(uriFull, uriRemnant):
            if resolver is not None:
                return resolver.resolveExtended(uriFull, subURI, **kw)

        if self.containsLocal(uriFull, uriRemnant, **kw):
            return self.resolveLocal(uriFull, uriRemnant, **kw)

        if uriFull == uriRemnant:
            return self.resolveFromHost(uriFull, **kw)
        else:
            raise URIResolutionError(uriFull, self)

    def containsLocal(self, uriFull, uriRemnant, **kw):
        return False
    def resolveLocal(self, uriFull, uriRemnant, **kw):
        raise URIResolutionError(uriFull, self, 'Not resolvable local to this node')

    def containsExtended(self, uriFull, uriRemnant):
        for subURI, resolver in self.iterResolversForURI(uri):
            if resolver is not None:
                return True
        return self.containsLocal(uriFull, uriRemnant)

    def getResolversForURI(self, uriFull, uriRemnant):
        return list(self.iterResolversForURI(uriFull, uriRemnant))
    def iterResolversForURI(self, uriFull, uriRemnant):
        """Generator of (resolver, uriRemnant) collection"""
        raise NotImplementedError('Subclass Responsibility')

