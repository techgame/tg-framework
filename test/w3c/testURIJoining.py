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

from TG.common.testPackageRunner import TestSuite, FunctionTestCase, TestProgram

from TG.w3c import uri

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TestURIJoining(TestSuite):
    baseURI = uri.URI('http://a/b/c/d;p?q#f')

    uriTests = """
        g:h        = <URI:g:h>
        //g        = <URI:http://g>
        g          = <URI:http://a/b/c/g>
        ./g        = <URI:http://a/b/c/g>
        g/         = <URI:http://a/b/c/g/>
        /g         = <URI:http://a/g>
        ?y         = <URI:http://a/b/c/d;p?y>
        g?y        = <URI:http://a/b/c/g?y>
        g?y/./x    = <URI:http://a/b/c/g?y/./x>
        #s         = <URI:http://a/b/c/d;p?q#s>
        g#s        = <URI:http://a/b/c/g#s>
        g#s/./x    = <URI:http://a/b/c/g#s/./x>
        g?y#s      = <URI:http://a/b/c/g?y#s>
        ;x         = <URI:http://a/b/c/d;x>
        g;x        = <URI:http://a/b/c/g;x>
        g;x?y#s    = <URI:http://a/b/c/g;x?y#s>
        .          = <URI:http://a/b/c/>
        ./         = <URI:http://a/b/c/>
        ..         = <URI:http://a/b/>
        ../        = <URI:http://a/b/>
        ../g       = <URI:http://a/b/g>
        ../..      = <URI:http://a/>
        ../../     = <URI:http://a/>
        ../../g    = <URI:http://a/g>
        """
    uriTests = filter(None, map(str.strip, uriTests.split('\n')))
    uriTests = [map(str.strip, [x for x in test.split('=')]) for test in uriTests ]

    def _generateURLJoinTest(self, uriEmbedded, uriResult):
        return lambda:self._testURLJoin(uriEmbedded, uriResult)

    def generateTests(self):
        for uriEmbedded, uriResult in self.uriTests:
            testfn = FunctionTestCase(self._generateURLJoinTest(uriEmbedded, uriResult),
                    description='URL join of %r and \'%s\' should = \'%s\' '%(self.baseURI, uriEmbedded, uriResult))
            self.addTest(testfn)

    def _testURLJoin(self, uriEmbedded, uriResult):
        joinedURI = self.baseURI.join(uriEmbedded)
        if repr(joinedURI) != uriResult:
            print
            print 'B:', repr(self.baseURI)
            print 'E:', uriEmbedded
            print 'T:', uriResult
            print '?:', repr(joinedURI)
            print 'D:', ''.join([(a==b and '1' or '0') for a,b in map(None, repr(joinedURI), uriResult)])
            print
        #else:
        #    print "%r + %r == %r" % (self.baseURI, uriEmbedded, joinedURI)

        assert repr(joinedURI) == uriResult, "Joined URI does not matched prescribed URI form!"

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Unittest Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    TestProgram()

