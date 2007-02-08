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

from TG.uriResolver import URIResolutionError
from TG.uriResolver.fileobj import FileResolver

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TestFileResolver(unittest.TestCase):
    def getTestPath(self):
        return os.path.join(workingPath, '..')
    def setUp(self):
        self.resolver = FileResolver('/usr/local/', self.getTestPath())
    def tearDown(self):
        del self.resolver

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testExistingFile(self):
        resource = self.resolver.resolve('/usr/local/common/all.py')
        self.failUnless(resource.exists())
        self.failUnless(resource.open().read().startswith('#!/usr/bin/env python'))

    def testExistingRelativeFile(self):
        resourceOne = self.resolver.resolve('/usr/local/common/all.py')
        resourceTwo = resourceOne.resolve('../uriResolver/testFilesystem.py')
        self.failUnless(resourceTwo.exists())
        self.failUnless(resourceTwo.open().read().startswith('#!/usr/bin/env python'))

    def testNonExistingFile(self):
        self.failUnlessRaises(URIResolutionError, self.resolver.resolve, '/usr/local/does not exist.txt')

    def testExistingDirectory(self):
        resource = self.resolver.resolve('/usr/local/common/')
        self.failUnless(resource.exists())

    def testExistingDirectoryRelative(self):
        resource = self.resolver.resolve('/usr/local/common/')
        self.failUnless(resource.exists())

        resourceOne = resource.resolve('all.py')
        self.failUnless(resourceOne.exists())

        self.failUnlessRaises(URIResolutionError, resource.resolve, 'does not exist.txt')

    def testNonExistingDirectory(self):
        self.failUnlessRaises(URIResolutionError, self.resolver.resolve, '/usr/local/does not exist/')

    def testInvalidURI(self):
        self.failUnlessRaises(URIResolutionError, self.resolver.resolve, '/usr/ports')
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Unittest Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    workingPath = os.getcwd()
    unittest.main()
else:
    workingPath = os.path.dirname(__file__)

