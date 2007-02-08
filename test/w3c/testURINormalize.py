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

from TG.common.testPackageRunner import TestSuite, FunctionTestCase, TestCase, TestProgram

from TG.w3c import uri

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TestURINormalization(TestSuite):
    baseURI = uri.URI('http://a/b/c/d;p?q#f')
    uriTests = """
        .          = 
        ./         = 
        ./.        = 
        ..         = ../
        ../        = ../
        ../.       = ../
        ../g       = ../g
        ../g/      = ../g/
        ../g/.     = ../g/
        ../..      = ../../
        ../../     = ../../
        ../../.    = ../../
        ../../g    = ../../g
        """
    uriTests = filter(None, map(str.strip, uriTests.split('\n')))
    uriTests = [map(str.strip, test.split('=')) for test in uriTests]

    def _generateURLNormalizedPathTest(self, uriTest, uriResult):
        return lambda:self._testURLNormalizedPath(uriTest, uriResult)

    def generateTests(self):
        for uriTest, uriResult in self.uriTests:
            testfn = FunctionTestCase(self._generateURLNormalizedPathTest(uriTest, uriResult),
                    description='URL join of %r and \'%s\' should = \'%s\' '%(self.baseURI, uriTest, uriResult))
            self.addTest(testfn)

    def _testURLNormalizedPath(self, uriTest, uriResult):
        normURI = uri.URI(uriTest)
        normURI.normalizePath()
        normURI = str(normURI)
        if normURI != uriResult:
            print
            print 'E:', uriTest
            print 'T:', uriResult
            print '?:', normURI
            print 'D:', ''.join([(a==b and '1' or '0') for a,b in map(None, normURI, uriResult)])
            print

        assert normURI == uriResult, "Joined URI does not matched prescribed URI form!"


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Unittest Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    TestProgram()

