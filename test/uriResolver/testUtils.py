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
from TG.uriResolver.utils import FilenameURIResolver

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class FilenameURIResolver_TEST(FilenameURIResolver):
    def resolveExtended(self, uriFull, uriRemnant, **kw):
        # Just return the constructed URI for our test
        return uriFull

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TestFilenameURIResolver(unittest.TestCase):
    def getTestPath(self):
        return self.joinTestPath('..')
    def joinTestPath(self, path):
        return os.path.join(workingPath, path)

    def setUp(self):
        self.resolver = FilenameURIResolver_TEST('scheme:/subdir/', self.getTestPath())

    def tearDown(self):
        del self.resolver

    def test__file__(self):
        fileNominal = os.path.splitext(__file__)[0]
        self.assertEqual(self.resolver.resolve(fileNominal), 'scheme:/subdir/uriResolver/testUtils')

    def testRelativeFile(self):
        self.assertEqual(self.resolver.resolve(self.joinTestPath('../common/all.py')), 'scheme:/subdir/common/all.py')

    def testRelativeDir(self):
        self.assertEqual(self.resolver.resolve(self.joinTestPath('../common')), 'scheme:/subdir/common')
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Unittest Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    workingPath = os.getcwd()
    unittest.main()
else:
    workingPath = os.path.dirname(__file__)

