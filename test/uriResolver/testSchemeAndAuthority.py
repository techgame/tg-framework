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

class TestSchemeAndAuthority(unittest.TestCase):
    def printResolver(self, resolver):
        print
        print 'Resolver:', resolver
        for each in resolver.getChildResolvers().items():
            print '   ',each
        print

    def testSchemeErrors(self):
        resolver = uriResolver.SchemeResolver()

        self.assertRaises(uriResolver.URIResolutionError, resolver.resolve, '')
        self.assertRaises(uriResolver.URIResolutionError, resolver.resolve, '/not/exist')
        self.assertRaises(uriResolver.URIResolutionError, resolver.resolve, 'does:/not/exist')
        self.assertRaises(uriResolver.URIResolutionError, resolver.resolve, 'does://not/exist')
     
    def testAuthorityErrors(self):
        resolver = uriResolver.AuthorityResolver()

        self.assertRaises(uriResolver.URIResolutionError, resolver.resolve, '')
        self.assertRaises(uriResolver.URIResolutionError, resolver.resolve, '/not/exist')
        self.assertRaises(uriResolver.URIResolutionError, resolver.resolve, 'does:/not/exist')
        self.assertRaises(uriResolver.URIResolutionError, resolver.resolve, 'does://not/exist')

    def testSchemeAuthorityErrors(self):
        resolver = uriResolver.SchemeAuthorityResolver()

        self.assertRaises(uriResolver.URIResolutionError, resolver.resolve, '')
        self.assertRaises(uriResolver.URIResolutionError, resolver.resolve, '/not/exist')
        self.assertRaises(uriResolver.URIResolutionError, resolver.resolve, 'does:/not/exist')
        self.assertRaises(uriResolver.URIResolutionError, resolver.resolve, 'does://not/exist')
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testSchemeDefault(self):
        resolver = uriResolver.SchemeResolver()
        defTestResolver = TestResolverEndpoint('def')
        resolver.addDefaultResolver(defTestResolver)
    
        self.assertEqual(resolver.resolve(''), defTestResolver)
        self.assertEqual(resolver.resolve('/not/exist'), defTestResolver)
        self.assertRaises(uriResolver.URIResolutionError, resolver.resolve, 'does:/not/exist')
        self.assertRaises(uriResolver.URIResolutionError, resolver.resolve, 'does://not/exist')

    def testAuthorityDefault(self):
        resolver = uriResolver.AuthorityResolver()
        defTestResolver = TestResolverEndpoint('def')
        resolver.addDefaultResolver(defTestResolver)
    
        self.assertEqual(resolver.resolve(''), defTestResolver)
        self.assertEqual(resolver.resolve('/not/exist'), defTestResolver)
        self.assertEqual(resolver.resolve('does:/not/exist'), defTestResolver)
        self.assertRaises(uriResolver.URIResolutionError, resolver.resolve, 'does://not/exist')

    def testSchemeAuthorityDefault(self):
        resolver = uriResolver.SchemeAuthorityResolver()
        defTestResolver = TestResolverEndpoint('def')
        resolver.addDefaultResolver(defTestResolver)
    
        self.assertEqual(resolver.resolve(''), defTestResolver)
        self.assertEqual(resolver.resolve('/not/exist'), defTestResolver)
        self.assertRaises(uriResolver.URIResolutionError, resolver.resolve, 'does:/not/exist')
        self.assertRaises(uriResolver.URIResolutionError, resolver.resolve, 'does://not/exist')

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testScheme(self):
        resolver = uriResolver.SchemeResolver()

        skinTestResolver = TestResolverEndpoint('skin')
        resolver.addResolverForURI(skinTestResolver, 'skin:')

        objTestResolver = TestResolverEndpoint('obj')
        resolver.addResolverForURI(objTestResolver, 'obj:')

        defTestResolver = TestResolverEndpoint('def')
        resolver.addDefaultResolver(defTestResolver)
    
        self.assertEqual(resolver.resolve('skin:'), skinTestResolver)
        self.assertEqual(resolver.resolve('skin:/path'), skinTestResolver)
        self.assertEqual(resolver.resolve('skin://auth'), skinTestResolver)
        self.assertEqual(resolver.resolve('skin://auth/path'), skinTestResolver)

        self.assertEqual(resolver.resolve('obj:'), objTestResolver)
        self.assertEqual(resolver.resolve('obj:/path'), objTestResolver)
        self.assertEqual(resolver.resolve('obj://auth'), objTestResolver)
        self.assertEqual(resolver.resolve('obj://auth/path'), objTestResolver)
        
        self.assertRaises(uriResolver.URIResolutionError, resolver.resolve, 'dne:')
        self.assertRaises(uriResolver.URIResolutionError, resolver.resolve, 'dne:/path')
        self.assertRaises(uriResolver.URIResolutionError, resolver.resolve, 'dne://auth')
        self.assertRaises(uriResolver.URIResolutionError, resolver.resolve, 'dne://auth/path')
        
        self.assertEqual(resolver.resolve(''), defTestResolver)
        self.assertEqual(resolver.resolve('/path'), defTestResolver)
        self.assertEqual(resolver.resolve('//auth'), defTestResolver)
        self.assertEqual(resolver.resolve('//auth/path'), defTestResolver)

    def testAuthority(self):
        resolver = uriResolver.AuthorityResolver()

        authTestResolver = TestResolverEndpoint('auth')
        resolver.addResolverForURI(authTestResolver, '//auth')

        defTestResolver = TestResolverEndpoint('def')
        resolver.addDefaultResolver(defTestResolver)

        self.assertEqual(resolver.resolve('skin:'), defTestResolver)
        self.assertEqual(resolver.resolve('skin:/path'), defTestResolver)
        self.assertEqual(resolver.resolve('skin://auth'), authTestResolver)
        self.assertEqual(resolver.resolve('skin://auth/path'), authTestResolver)

        self.assertEqual(resolver.resolve('obj:'), defTestResolver)
        self.assertEqual(resolver.resolve('obj:/path'), defTestResolver)
        self.assertEqual(resolver.resolve('obj://auth'), authTestResolver)
        self.assertEqual(resolver.resolve('obj://auth/path'), authTestResolver)
    
        self.assertEqual(resolver.resolve('dne:'), defTestResolver)
        self.assertEqual(resolver.resolve('dne:/path'), defTestResolver)
        self.assertEqual(resolver.resolve('dne://auth'), authTestResolver)
        self.assertEqual(resolver.resolve('dne://auth/path'), authTestResolver)
        self.assertRaises(uriResolver.URIResolutionError, resolver.resolve, 'dne://DNEauth')
        self.assertRaises(uriResolver.URIResolutionError, resolver.resolve, 'dne://DNEauth/path')
    
        self.assertEqual(resolver.resolve(''), defTestResolver)
        self.assertEqual(resolver.resolve('/path'), defTestResolver)
        self.assertEqual(resolver.resolve('//auth'), authTestResolver)
        self.assertEqual(resolver.resolve('//auth/path'), authTestResolver)
    
    def testSchemeAuthority(self):
        resolver = uriResolver.SchemeAuthorityResolver()

        skinAuthTestResolver = TestResolverEndpoint('skin://auth')
        resolver.addResolverForURI(skinAuthTestResolver, 'skin://auth')

        skinDefTestResolver = TestResolverEndpoint('skin://')
        resolver.addResolverForURI(skinDefTestResolver, 'skin:')

        defAuthTestResolver = TestResolverEndpoint('//auth')
        resolver.addResolverForURI(defAuthTestResolver, '//auth')

        defTestResolver = TestResolverEndpoint('def')
        resolver.addDefaultResolver(defTestResolver)

        self.assertEqual(resolver.resolve('skin:'), skinDefTestResolver)
        self.assertEqual(resolver.resolve('skin:/path'), skinDefTestResolver)
        self.assertEqual(resolver.resolve('skin://auth'), skinAuthTestResolver)
        self.assertEqual(resolver.resolve('skin://auth/path'), skinAuthTestResolver)

        self.assertRaises(uriResolver.URIResolutionError, resolver.resolve, 'dne:')
        self.assertRaises(uriResolver.URIResolutionError, resolver.resolve, 'dne:/path')
        self.assertRaises(uriResolver.URIResolutionError, resolver.resolve, 'dne://auth')
        self.assertRaises(uriResolver.URIResolutionError, resolver.resolve, 'dne://auth/path')
    
        self.assertEqual(resolver.resolve(''), defTestResolver)
        self.assertEqual(resolver.resolve('/path'), defTestResolver)
        self.assertEqual(resolver.resolve('//auth'), defAuthTestResolver)
        self.assertEqual(resolver.resolve('//auth/path'), defAuthTestResolver)
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Unittest Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    unittest.main()

