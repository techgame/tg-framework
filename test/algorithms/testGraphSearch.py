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
from TG.algorithms import graphSearch

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TestNode(graphSearch.GraphNode):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__, self.name)

class TestGraphSearch(unittest.TestCase):
    def myVisitor(self, node, result):
        result.append(node.name)
        return result

    def setUp(self):
        a = TestNode('A')
        b = TestNode('B')
        c = TestNode('C')
        a.linkTo(b)
        b.linkTo(c)
        c.linkTo(a)

        self.a = a
        self.b = b
        self.c = c

    def tearDown(self):
        pass

    def testAOutbound(self):
        outbound = graphSearch.OutboundGraphSearch()
        self.assertEqual(outbound(self.a, self.myVisitor, []), list('ABC'))
    def testAInbound(self):
        inbound = graphSearch.InboundGraphSearch()
        self.assertEqual(inbound(self.a, self.myVisitor, []), list('ACB'))
    def testAInorder(self):
        inorder = graphSearch.InOrderGraphSearch()
        self.assertEqual(inorder(self.a, self.myVisitor, []), list('BCA'))

    def testBOutbound(self):
        outbound = graphSearch.OutboundGraphSearch()
        self.assertEqual(outbound(self.b, self.myVisitor, []), list('BCA'))
    def testBInbound(self):
        inbound = graphSearch.InboundGraphSearch()
        self.assertEqual(inbound(self.b, self.myVisitor, []), list('BAC'))
    def testBInorder(self):
        inorder = graphSearch.InOrderGraphSearch()
        self.assertEqual(inorder(self.b, self.myVisitor, []), list('CAB'))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testUnlinkedAOutbound(self):
        self.c.unlinkTo(self.a)
        outbound = graphSearch.OutboundGraphSearch()
        self.assertEqual(outbound(self.a, self.myVisitor, []), list('ABC'))
    def testUnlinkedAInbound(self):
        self.c.unlinkTo(self.a)
        inbound = graphSearch.InboundGraphSearch()
        self.assertEqual(inbound(self.a, self.myVisitor, []), list('A'))
    def testUnlinkedAInorder(self):
        self.c.unlinkTo(self.a)
        inorder = graphSearch.InOrderGraphSearch()
        self.assertEqual(inorder(self.a, self.myVisitor, []), list('ABC'))

    def testUnlinkedBOutbound(self):
        self.c.unlinkTo(self.a)
        outbound = graphSearch.OutboundGraphSearch()
        self.assertEqual(outbound(self.b, self.myVisitor, []), list('BC'))
    def testUnlinkedBInbound(self):
        self.c.unlinkTo(self.a)
        inbound = graphSearch.InboundGraphSearch()
        self.assertEqual(inbound(self.b, self.myVisitor, []), list('BA'))
    def testUnlinkedBInorder(self):
        self.c.unlinkTo(self.a)
        inorder = graphSearch.InOrderGraphSearch()
        self.assertEqual(inorder(self.b, self.myVisitor, []), list('ABC'))
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Unittest Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    unittest.main()
