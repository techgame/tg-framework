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

from TG.w3c import uri

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TestURIPathDefaultTestCase(unittest.TestCase):
    def verifyURIParts(self, uriValue, scheme, authority, path, query, fragment):
        try:
            self.failUnlessEqual(uriValue.scheme, scheme)
            self.failUnlessEqual(uriValue.authority, authority)
            self.failUnlessEqual(uriValue.path, path)
            self.failUnlessEqual(uriValue.query, query)
            self.failUnlessEqual(uriValue.fragment, fragment)
        except:
            print
            print uriValue.getURIParts()
            print
            raise

    def testScheme(self):
        'Path Default: "scheme:"'
        uriStr = 'scheme:'
        uriValue = uri.URIPathDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, 'scheme', None, None, None, None)

    def testPath(self):
        'Path Default: "path"'
        uriStr = 'path'
        uriValue = uri.URIPathDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, None, None, 'path', None, None)

    def testPathSlash(self):
        'Path Default: "/path"'
        uriStr = '/path'
        uriValue = uri.URIPathDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, None, None, '/path', None, None)

    def testSchemePath(self):
        'Path Default: "scheme:path"'
        uriStr = 'scheme:path'
        uriValue = uri.URIPathDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, 'scheme', None, 'path', None, None)

    def testSchemePathSlash(self):
        'Path Default: "scheme:/path"'
        uriStr = 'scheme:/path'
        uriValue = uri.URIPathDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, 'scheme', None, '/path', None, None)

    def testAuthority(self):
        'Path Default: "//authority"'
        uriStr = '//authority'
        uriValue = uri.URIPathDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, None, 'authority', None, None, None)

    def testSchemeAuthority(self):
        'Path Default: "scheme://authority"'
        uriStr = 'scheme://authority'
        uriValue = uri.URIPathDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, 'scheme', 'authority', None, None, None)

    def testAuthorityPath(self):
        'Path Default: "//authority/path"'
        uriStr = '//authority/path'
        uriValue = uri.URIPathDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, None, 'authority', '/path', None, None)

    def testSchemeAuthorityPath(self):
        'Path Default: "scheme://authority/path"'
        uriStr = 'scheme://authority/path'
        uriValue = uri.URIPathDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, 'scheme', 'authority', '/path', None, None)

    def testUserAuthorityPath(self):
        'Path Default: "//user@authority/path"'
        uriStr = '//user@authority/path'
        uriValue = uri.URIPathDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, None, 'user@authority', '/path', None, None)

    def testSchemeUserAuthorityPath(self):
        'Path Default: "scheme://user@authority/path"'
        uriStr = 'scheme://user@authority/path'
        uriValue = uri.URIPathDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, 'scheme', 'user@authority', '/path', None, None)

    def testSchemeUserAuthorityHostPath(self):
        'Path Default: "scheme://user@authority:4242/path"'
        uriStr = 'scheme://user@authority:4242/path'
        uriValue = uri.URIPathDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, 'scheme', 'user@authority:4242', '/path', None, None)

    def testMailto(self):
        'Path Default: "mailto:user@host"'
        uriStr = 'mailto:user@host'
        uriValue = uri.URIPathDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, 'mailto', None, 'user@host', None, None)

    def testUserPasswdAuthority(self):
        'Path Default: "//user:passwd@authority"'
        uriStr = '//user:passwd@authority'
        uriValue = uri.URIPathDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, None, 'user:passwd@authority', None, None, None)

    def testUserPasswdAuthorityHostPath(self):
        'Path Default: "//user:passwd@authority:4242/path"'
        uriStr = '//user:passwd@authority:4242/path'
        uriValue = uri.URIPathDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, None, 'user:passwd@authority:4242', '/path', None, None)

    def testSchemeUserPasswdAuthorityHostPath(self):
        'Path Default: "scheme://user:passwd@authority:4242/path"'
        uriStr = 'scheme://user:passwd@authority:4242/path'
        uriValue = uri.URIPathDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, 'scheme', 'user:passwd@authority:4242', '/path', None, None)

    def testSchemeUserPasswdAuthorityHostPathAttributes(self):
        'Path Default: "scheme://user:passwd@authority:4242/path;attr1=value1"'
        uriStr = 'scheme://user:passwd@authority:4242/path;attr1=value1'
        uriValue = uri.URIPathDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, 'scheme', 'user:passwd@authority:4242', '/path;attr1=value1', None, None)

    def testSchemeUserPasswdAuthorityHostPathAttributesQuery(self):
        'Path Default: "scheme://user:passwd@authority:4242/path;attr1=value1?query"'
        uriStr = 'scheme://user:passwd@authority:4242/path;attr1=value1?query'
        uriValue = uri.URIPathDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, 'scheme', 'user:passwd@authority:4242', '/path;attr1=value1', 'query', None)

    def testSchemeUserPasswdAuthorityHostPathAttributesQueryFragment(self):
        'Path Default: "scheme://user:passwd@authority:4242/path;attr1=value1?query#fragment"'
        uriStr = 'scheme://user:passwd@authority:4242/path;attr1=value1?query#fragment'
        uriValue = uri.URIPathDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, 'scheme', 'user:passwd@authority:4242', '/path;attr1=value1', 'query', 'fragment')

    def testSchemeNullAuthorityPathAttributesQueryFragment(self):
        'Path Default: "scheme:///path;attr1=value1?query#fragment"'
        uriStr = 'scheme:///path;attr1=value1?query#fragment'
        uriValue = uri.URIPathDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, 'scheme', '', '/path;attr1=value1', 'query', 'fragment')

    def testSchemePathAttributesQueryFragment(self):
        'Path Default: "scheme:/path;attr1=value1?query#fragment"'
        uriStr = 'scheme:/path;attr1=value1?query#fragment'
        uriValue = uri.URIPathDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, 'scheme', None, '/path;attr1=value1', 'query', 'fragment')

    def testNullAuthorityPathAttributesQueryFragment(self):
        'Path Default: "///path;attr1=value1?query#fragment"'
        uriStr = '///path;attr1=value1?query#fragment'
        uriValue = uri.URIPathDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, None, '', '/path;attr1=value1', 'query', 'fragment')

    def testPathAttributesQueryFragment(self):
        'Path Default: "/path;attr1=value1?query#fragment"'
        uriStr = '/path;attr1=value1?query#fragment'
        uriValue = uri.URIPathDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, None, None, '/path;attr1=value1', 'query', 'fragment')

    def testPathQueryFragment(self):
        'Path Default: "/path?query#fragment"'
        uriStr = '/path?query#fragment'
        uriValue = uri.URIPathDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, None, None, '/path', 'query', 'fragment')

    def testQueryFragment(self):
        'Path Default: "?query#fragment"'
        uriStr = '?query#fragment'
        uriValue = uri.URIPathDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, None, None, None, 'query', 'fragment')

    def testSchemeQuery(self):
        'Path Default: "scheme:?query"'
        uriStr = 'scheme:?query'
        uriValue = uri.URIPathDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, 'scheme', None, None, 'query', None)

    def testQuery(self):
        'Path Default: "?query"'
        uriStr = '?query'
        uriValue = uri.URIPathDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, None, None, None, 'query', None)

    def testFragment(self):
        'Path Default: "#fragment"'
        uriStr = '#fragment'
        uriValue = uri.URIPathDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, None, None, None, None, 'fragment')

    def testSchemeFragment(self):
        'Path Default: "scheme:#fragment"'
        uriStr = 'scheme:#fragment'
        uriValue = uri.URIPathDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, 'scheme', None, None, None, 'fragment')

    def testPathQuery(self):
        'Path Default: "/path?query"'
        uriStr = '/path?query'
        uriValue = uri.URIPathDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, None, None, '/path', 'query', None)

    def testPathFragment(self):
        'Path Default: "/path#fragment"'
        uriStr = '/path#fragment'
        uriValue = uri.URIPathDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, None, None, '/path', None, 'fragment')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TestURIAuthorityDefaultTestCase(unittest.TestCase):
    def verifyURIParts(self, uriValue, scheme, authority, path, query, fragment):
        self.failUnlessEqual(uriValue.scheme, scheme)
        self.failUnlessEqual(uriValue.authority, authority)
        self.failUnlessEqual(uriValue.path, path)
        self.failUnlessEqual(uriValue.query, query)
        self.failUnlessEqual(uriValue.fragment, fragment)

    def testScheme(self):
        'Authority Default: "scheme:"'
        uriStr = 'scheme:'
        uriValue = uri.URIAuthorityDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, 'scheme', '', None, None, None)

    def testAuthority(self):
        'Authority Default: "authority"'
        uriStr = 'authority'
        uriValue = uri.URIAuthorityDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, None, 'authority', None, None, None)

    def testPath(self):
        'Authority Default: "/path"'
        uriStr = '/path'
        uriValue = uri.URIAuthorityDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, None, '', '/path', None, None)

    def testSchemeAuthority(self):
        'Authority Default: "scheme:authority"'
        uriStr = 'scheme:authority'
        uriValue = uri.URIAuthorityDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, 'scheme', 'authority', None, None, None)

    def testSchemePath(self):
        'Authority Default: "scheme:/path"'
        uriStr = 'scheme:/path'
        uriValue = uri.URIAuthorityDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, 'scheme', '', '/path', None, None)

    def testNetworkAuthority(self):
        'Authority Default: "//authority"'
        uriStr = '//authority'
        uriValue = uri.URIAuthorityDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, None, 'authority', None, None, None)

    def testSchemeNetworkAuthority(self):
        'Authority Default: "scheme://authority"'
        uriStr = 'scheme://authority'
        uriValue = uri.URIAuthorityDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, 'scheme', 'authority', None, None, None)

    def testAuthorityPath(self):
        'Authority Default: "authority/path"'
        uriStr = 'authority/path'
        uriValue = uri.URIAuthorityDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, None, 'authority', '/path', None, None)

    def testNetworkAuthorityPath(self):
        'Authority Default: "//authority/path"'
        uriStr = '//authority/path'
        uriValue = uri.URIAuthorityDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, None, 'authority', '/path', None, None)

    def testSchemeAuthorityPath(self):
        'Authority Default: "scheme:authority/path"'
        uriStr = 'scheme:authority/path'
        uriValue = uri.URIAuthorityDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, 'scheme', 'authority', '/path', None, None)

    def testSchemeNetworkAuthorityPath(self):
        'Authority Default: "scheme://authority/path"'
        uriStr = 'scheme://authority/path'
        uriValue = uri.URIAuthorityDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, 'scheme', 'authority', '/path', None, None)

    def testNetworkUserAuthorityPath(self):
        'Authority Default: "//user@authority/path"'
        uriStr = '//user@authority/path'
        uriValue = uri.URIAuthorityDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, None, 'user@authority', '/path', None, None)

    def testUserAuthorityPath(self):
        'Authority Default: "user@authority/path"'
        uriStr = 'user@authority/path'
        uriValue = uri.URIAuthorityDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, None, 'user@authority', '/path', None, None)

    def testSchemeUserAuthorityPath(self):
        'Authority Default: "scheme:user@authority/path"'
        uriStr = 'scheme:user@authority/path'
        uriValue = uri.URIAuthorityDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, 'scheme', 'user@authority', '/path', None, None)

    def testSchemeNetworkUserAuthorityPath(self):
        'Authority Default: "scheme://user@authority/path"'
        uriStr = 'scheme://user@authority/path'
        uriValue = uri.URIAuthorityDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, 'scheme', 'user@authority', '/path', None, None)

    def testSchemeNetworkUserAuthorityHostPath(self):
        'Authority Default: "scheme://user@authority:4242/path"'
        uriStr = 'scheme://user@authority:4242/path'
        uriValue = uri.URIAuthorityDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, 'scheme', 'user@authority:4242', '/path', None, None)

    def testSchemeUserAuthorityHostPath(self):
        'Authority Default: "scheme:user@authority:4242/path"'
        uriStr = 'scheme:user@authority:4242/path'
        uriValue = uri.URIAuthorityDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, 'scheme', 'user@authority:4242', '/path', None, None)

    def testMailto(self):
        'Authority Default: "mailto:user@host"'
        uriStr = 'mailto:user@host'
        uriValue = uri.URIAuthorityDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, 'mailto', 'user@host', None, None, None)

    def testNetworkUserPasswdAuthority(self):
        'Authority Default: "//user:passwd@authority"'
        uriStr = '//user:passwd@authority'
        uriValue = uri.URIAuthorityDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, None, 'user:passwd@authority', None, None, None)

    def testNetworkUserPasswdAuthorityHostPath(self):
        'Authority Default: "//user:passwd@authority:4242/path"'
        uriStr = '//user:passwd@authority:4242/path'
        uriValue = uri.URIAuthorityDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, None, 'user:passwd@authority:4242', '/path', None, None)

    def testSchemeNetworkUserPasswdAuthorityHostPath(self):
        'Authority Default: "scheme://user:passwd@authority:4242/path"'
        uriStr = 'scheme://user:passwd@authority:4242/path'
        uriValue = uri.URIAuthorityDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, 'scheme', 'user:passwd@authority:4242', '/path', None, None)

    def testSchemeUserPasswdAuthorityHostPath(self):
        'Authority Default: "scheme:user:passwd@authority:4242/path"'
        uriStr = 'scheme:user:passwd@authority:4242/path'
        uriValue = uri.URIAuthorityDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, 'scheme', 'user:passwd@authority:4242', '/path', None, None)

    def testSchemeNetworkUserPasswdAuthorityHostPathAttributes(self):
        'Authority Default: "scheme://user:passwd@authority:4242/path;attr1=value1"'
        uriStr = 'scheme://user:passwd@authority:4242/path;attr1=value1'
        uriValue = uri.URIAuthorityDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, 'scheme', 'user:passwd@authority:4242', '/path;attr1=value1', None, None)

    def testSchemeUserPasswdAuthorityHostPathAttributes(self):
        'Authority Default: "scheme:user:passwd@authority:4242/path;attr1=value1"'
        uriStr = 'scheme:user:passwd@authority:4242/path;attr1=value1'
        uriValue = uri.URIAuthorityDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, 'scheme', 'user:passwd@authority:4242', '/path;attr1=value1', None, None)

    def testSchemeNetworkUserPasswdAuthorityHostPathAttributesQuery(self):
        'Authority Default: "scheme://user:passwd@authority:4242/path;attr1=value1?query"'
        uriStr = 'scheme://user:passwd@authority:4242/path;attr1=value1?query'
        uriValue = uri.URIAuthorityDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, 'scheme', 'user:passwd@authority:4242', '/path;attr1=value1', 'query', None)

    def testSchemeUserPasswdAuthorityHostPathAttributesQuery(self):
        'Authority Default: "scheme:user:passwd@authority:4242/path;attr1=value1?query"'
        uriStr = 'scheme:user:passwd@authority:4242/path;attr1=value1?query'
        uriValue = uri.URIAuthorityDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, 'scheme', 'user:passwd@authority:4242', '/path;attr1=value1', 'query', None)

    def testSchemeNetworkUserPasswdAuthorityHostPathAttributesQueryFragment(self):
        'Authority Default: "scheme://user:passwd@authority:4242/path;attr1=value1?query#fragment"'
        uriStr = 'scheme://user:passwd@authority:4242/path;attr1=value1?query#fragment'
        uriValue = uri.URIAuthorityDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, 'scheme', 'user:passwd@authority:4242', '/path;attr1=value1', 'query', 'fragment')

    def testSchemeUserPasswdAuthorityHostPathAttributesQueryFragment(self):
        'Authority Default: "scheme:user:passwd@authority:4242/path;attr1=value1?query#fragment"'
        uriStr = 'scheme:user:passwd@authority:4242/path;attr1=value1?query#fragment'
        uriValue = uri.URIAuthorityDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, 'scheme', 'user:passwd@authority:4242', '/path;attr1=value1', 'query', 'fragment')

    def testSchemeNetworkNullAuthorityPathAttributesQueryFragment(self):
        'Authority Default: "scheme:///path;attr1=value1?query#fragment"'
        uriStr = 'scheme:///path;attr1=value1?query#fragment'
        uriValue = uri.URIAuthorityDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, 'scheme', '', '/path;attr1=value1', 'query', 'fragment')

    def testSchemePathAttributesQueryFragment(self):
        'Authority Default: "scheme:/path;attr1=value1?query#fragment"'
        uriStr = 'scheme:/path;attr1=value1?query#fragment'
        uriValue = uri.URIAuthorityDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, 'scheme', '', '/path;attr1=value1', 'query', 'fragment')

    def testNetworkNullAuthorityPathAttributesQueryFragment(self):
        'Authority Default: "///path;attr1=value1?query#fragment"'
        uriStr = '///path;attr1=value1?query#fragment'
        uriValue = uri.URIAuthorityDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, None, '', '/path;attr1=value1', 'query', 'fragment')

    def testPathAttributesQueryFragment(self):
        'Authority Default: "/path;attr1=value1?query#fragment"'
        uriStr = '/path;attr1=value1?query#fragment'
        uriValue = uri.URIAuthorityDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, None, '', '/path;attr1=value1', 'query', 'fragment')

    def testPathQueryFragment(self):
        'Authority Default: "/path?query#fragment"'
        uriStr = '/path?query#fragment'
        uriValue = uri.URIAuthorityDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, None, '', '/path', 'query', 'fragment')

    def testQueryFragment(self):
        'Authority Default: "?query#fragment"'
        uriStr = '?query#fragment'
        uriValue = uri.URIAuthorityDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, None, '', None, 'query', 'fragment')

    def testSchemeQuery(self):
        'Authority Default: "scheme:?query"'
        uriStr = 'scheme:?query'
        uriValue = uri.URIAuthorityDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, 'scheme', '', None, 'query', None)

    def testQuery(self):
        'Authority Default: "?query"'
        uriStr = '?query'
        uriValue = uri.URIAuthorityDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, None, '', None, 'query', None)

    def testFragment(self):
        'Authority Default: "#fragment"'
        uriStr = '#fragment'
        uriValue = uri.URIAuthorityDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, None, '', None, None, 'fragment')

    def testSchemeFragment(self):
        'Authority Default: "scheme:#fragment"'
        uriStr = 'scheme:#fragment'
        uriValue = uri.URIAuthorityDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, 'scheme', '', None, None, 'fragment')

    def testPathQuery(self):
        'Authority Default: "/path?query"'
        uriStr = '/path?query'
        uriValue = uri.URIAuthorityDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, None, '', '/path', 'query', None)

    def testPathFragment(self):
        'Authority Default: "/path#fragment"'
        uriStr = '/path#fragment'
        uriValue = uri.URIAuthorityDefault(uriStr)
        self.failUnlessEqual(uriValue.uri, uriStr)
        self.verifyURIParts(uriValue, None, '', '/path', None, 'fragment')


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Unittest Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    unittest.main()

