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

import os
import unittest

from TG.uriResolver import URIResolutionError, PathResolver
from TG.uriResolver.fileobj import FileResolver
from TG.uriResolver.fileobj.zip import ZipResolver

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TestExplicitMultiFileResolver(unittest.TestCase):
    def getZipFilename(self):
        return os.path.join(workingPath, 'ziptest.zip')
    def getTestPath(self):
        return os.path.join(workingPath, '..')

    def setUp(self):
        self.resolver = PathResolver('/usr/')
        self.resolver.mount(FileResolver('/usr/local/', self.getTestPath()), 'local')
        zf = ZipResolver('/usr/share/', self.getZipFilename())
        self.resolver.mount(zf, 'share')
        self.resolver.mount(zf, 'bonko')
    def tearDown(self):
        del self.resolver

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testExistingFile(self):
        resource = self.resolver.resolve('/usr/local/common/all.py')
        self.failUnless(resource.exists())
        self.failUnless(resource.open().read().startswith('#!/usr/bin/env python'))

    def testExistingFileInZip(self):
        resource = self.resolver.resolve('/usr/share/common/all.py')
        self.failUnless(resource.exists())
        self.failUnless(resource.open().read().startswith('#!/usr/bin/env python'))

    def testExistingFileAliasInZip(self):
        resource = self.resolver.resolve('/usr/bonko/common/all.py')
        self.failUnless(resource.exists())
        self.failUnless(resource.open().read().startswith('#!/usr/bin/env python'))

    def testNonExistingFile(self):
        self.failUnlessRaises(URIResolutionError, self.resolver.resolve, '/usr/local/does not exist.txt')

    def testNonExistingFileInZip(self):
        self.failUnlessRaises(URIResolutionError, self.resolver.resolve, '/usr/share/does not exist.txt')

    def testExistingDirectory(self):
        resource = self.resolver.resolve('/usr/local/common')
        self.failUnless(resource.exists())

    def testNonExistingDirectory(self):
        self.failUnlessRaises(URIResolutionError, self.resolver.resolve, '/usr/share/does not exist/')

    def testInvalidURI(self):
        self.failUnlessRaises(URIResolutionError, self.resolver.resolve, '/usr/ports')
        self.failUnlessRaises(URIResolutionError, self.resolver.resolve, '/left-field')
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Unittest Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    workingPath = os.getcwd()
    unittest.main()
else:
    workingPath = os.path.dirname(__file__)

