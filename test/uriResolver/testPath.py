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

import unittest

from TG import uriResolver
from TG.uriResolver import URIResolutionError
from TG.uriResolver.base import URIResolverBase

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TestResolverEndpoint(URIResolverBase):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__, self.name)
    def resolveExtended(self, uriFull, uriRemnant, **kw):
        return self

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TestPath(unittest.TestCase):
    def printResolver(self, resolver):
        print
        print 'Resolver:', resolver
        for each in resolver.getChildResolvers().items():
            print '   ',each
        print

    def testPathErrors(self):
        resolver = uriResolver.PathResolver()

        self.assertEqual(resolver.resolve(''), resolver)
        self.assertRaises(uriResolver.URIResolutionError, resolver.resolve, '/not/exist')
        self.assertRaises(uriResolver.URIResolutionError, resolver.resolve, 'does:/not/exist')
        self.assertRaises(uriResolver.URIResolutionError, resolver.resolve, 'does://not/exist')
    
    def testPathDefault(self):
        resolver = uriResolver.PathResolver()

        devTestResolver = TestResolverEndpoint('dev')
        resolver.addDefaultResolver(devTestResolver)
    
        self.assertEqual(resolver.resolve(''), devTestResolver)
        self.assertEqual(resolver.resolve('does:'), devTestResolver)
        self.assertEqual(resolver.resolve('does://auth'), devTestResolver)
        self.assertRaises(uriResolver.URIResolutionError, resolver.resolve, '/not/exist')
        self.assertRaises(uriResolver.URIResolutionError, resolver.resolve, 'does:/not/exist')
        self.assertRaises(uriResolver.URIResolutionError, resolver.resolve, 'does://not/exist')

    def testPath(self):
        resolver = uriResolver.PathResolver()

        usrTestResolver = TestResolverEndpoint('/usr')
        resolver.addResolverForURI(usrTestResolver, '/usr')

        pathTestResolver = TestResolverEndpoint('/path')
        resolver.addResolverForURI(pathTestResolver, '/path')

        devTestResolver = TestResolverEndpoint('dev')
        resolver.addDefaultResolver(devTestResolver)

        self.assertEqual(resolver.resolve('skin:'), devTestResolver)
        self.assertEqual(resolver.resolve('skin:/path'), pathTestResolver)
        self.assertEqual(resolver.resolve('skin://auth'), devTestResolver)
        self.assertEqual(resolver.resolve('skin://auth/path'), pathTestResolver)

        self.assertEqual(resolver.resolve('obj:/usr'), usrTestResolver)
        self.assertEqual(resolver.resolve('obj:/usr/stuff/more'), usrTestResolver)
        self.assertEqual(resolver.resolve('/usr/stuff/more'), usrTestResolver)
        self.assertEqual(resolver.resolve('//auth/usr/stuff'), usrTestResolver)
        self.assertEqual(resolver.resolve('obj://auth/usr/stuff'), usrTestResolver)
        
        self.assertEqual(resolver.resolve('dne:'), devTestResolver)
        self.assertEqual(resolver.resolve('dne:/path'), pathTestResolver)
        self.assertEqual(resolver.resolve('dne://auth'), devTestResolver)
        self.assertEqual(resolver.resolve('dne://auth/path'), pathTestResolver)
        
        self.assertEqual(resolver.resolve(''), devTestResolver)
        self.assertEqual(resolver.resolve('/path'), pathTestResolver)
        self.assertEqual(resolver.resolve('//auth'), devTestResolver)
        self.assertEqual(resolver.resolve('//auth/path'), pathTestResolver)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Unittest Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    unittest.main()


