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
from TG.uriResolver.fileobj.zip import ZipResolver

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TestZipResolver(unittest.TestCase):
    def getZipFilename(self):
        return os.path.join(workingPath, 'ziptest.zip')
    def setUp(self):
        self.resolver = ZipResolver('/usr/local', self.getZipFilename())
    def tearDown(self):
        del self.resolver

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testExistingFile(self):
        resource = self.resolver.resolve('/usr/local/common/all.py')
        self.failUnless(resource.exists())
        self.failUnless(resource.open().read().startswith('#!/usr/bin/env python'))

    def testExistingRelativeFile(self):
        resource = self.resolver.resolve('/usr/local/common/all.py')

        resourceOne = resource.resolve('../__init__.py')
        self.failUnless(resource.exists())
        self.failUnless(resource.open().read().startswith('#!/usr/bin/env python'))

    def testNonExistingFile(self):
        self.failUnlessRaises(URIResolutionError, self.resolver.resolve, '/usr/local/does not exist.txt')

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

