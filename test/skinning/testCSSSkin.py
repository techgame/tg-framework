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

from TG.skinning.engine.xmlSkinner import XMLSkinner

import cssTestSkin as CSSTestSkin
from cssTestSkin.root import root
from cssTestSkin.test import test
from cssTestSkin.style import style

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def getNested(owner, *addrs):
    for addr in addrs:
        owner = owner.getChildren()[addr]
    return owner

class TestCSSSkin(unittest.TestCase):
    def setUp(self):
        self.skinner = XMLSkinner().installSkins(CSSTestSkin, namespace=None)

    def tearDown(self):
        del self.skinner

    def iterAuthor(self, result):
        author = result.ctx.getCSSCascade().author
        return author.normal.items()

    def testOverall(self):
        testSkin = """<?xml version='1.0'?>
        <root>
            <style>test {value: 1}</style>
            <test />
            <test id='myId'/>
            <test class='myClass'/>
            <test class='myClass myOtherClass'/>
            <test id='myId' class='myClass'/>
        </root>
        """
        result = self.skinner.skin(testSkin)
        self.assertEqual(type(result), root)
        self.assertEqual(type(getNested(result, 0)), style)

        for selector, declarations in self.iterAuthor(result):
            self.assertEqual(declarations , {'value':'1'})
            self.assertEqual(selector.name, 'test')
            self.assertEqual(selector.namespace, None)
            self.assertEqual(selector.qualifiers, ())

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        for testNode in result.getChildren()[1:]:
            testElemIF = testNode.getCSSElement()
            self.assertEqual(type(testNode), test)
            self.assertEqual(selector.matches(testElemIF), True, 'test{value:1} should apply to <test/> element: %r' % testNode)
    
    def testAny(self):
        testSkin = """<?xml version='1.0'?>
        <root>
            <style>*{value: 1}</style>

            <test />
            <test id='myId'/>
            <test class='myClass'/>
            <test class='myClass myOtherClass'/>
            <test id='myId' class='myClass'/>
        </root>
        """
        result = self.skinner.skin(testSkin)
        (selector, declarations), = self.iterAuthor(result)

        for testNode in result.getChildren()[1:]:
            testElemIF = testNode.getCSSElement()
            self.assertEqual(type(testNode), test)
            self.assertEqual(selector.matches(testElemIF), True, 'test{value:1} should apply to <test/> element: %r' % testNode)

    def testAnyId(self):
        testSkin = """<?xml version='1.0'?>
        <root>
            <style>#myId {value: 1}</style>

            <test />
            <test id='myId'/>
        </root>
        """
        result = self.skinner.skin(testSkin)
        (selector, declarations), = self.iterAuthor(result)

        testElemIF = getNested(result, 1).getCSSElement()
        self.assertEqual(selector.matches(testElemIF), False)

        testElemIF = getNested(result, 2).getCSSElement()
        self.assertEqual(selector.matches(testElemIF), True)

    def testId(self):
        testSkin = """<?xml version='1.0'?>
        <root>
            <style>test#myId {value: 1}</style>

            <test />
            <test id='myId'/>
        </root>
        """
        result = self.skinner.skin(testSkin)
        (selector, declarations), = self.iterAuthor(result)

        testElemIF = getNested(result, 1).getCSSElement()
        self.assertEqual(selector.matches(testElemIF), False)

        testElemIF = getNested(result, 2).getCSSElement()
        self.assertEqual(selector.matches(testElemIF), True)

    def testClass(self):
        testSkin = """<?xml version='1.0'?>
        <root>
            <style>test.myClass {value: 1}</style>

            <test />
            <test class='myClass'/>
            <test class='myClass myOtherClass'/>
        </root>
        """
        result = self.skinner.skin(testSkin)
        (selector, declarations), = self.iterAuthor(result)

        testElemIF = getNested(result, 1).getCSSElement()
        self.assertEqual(selector.matches(testElemIF), False)

        testElemIF = getNested(result, 2).getCSSElement()
        self.assertEqual(selector.matches(testElemIF), True)

        testElemIF = getNested(result, 3).getCSSElement()
        self.assertEqual(selector.matches(testElemIF), True)
            
    def testClassEx(self):
        testSkin = """<?xml version='1.0'?>
        <root>
            <style>test.myClass.myOtherClass {value: 1}</style>

            <test />
            <test class='myClass'/>
            <test class='myClass myOtherClass'/>
        </root>
        """
        result = self.skinner.skin(testSkin)
        (selector, declarations), = self.iterAuthor(result)

        testElemIF = getNested(result, 1).getCSSElement()
        self.assertEqual(selector.matches(testElemIF), False)

        testElemIF = getNested(result, 2).getCSSElement()
        self.assertEqual(selector.matches(testElemIF), False)

        testElemIF = getNested(result, 3).getCSSElement()
        self.assertEqual(selector.matches(testElemIF), True)
            
    def testClassId(self):
        testSkin = """<?xml version='1.0'?>
        <root>
            <style>test#myId.myClass {value: 1}</style>

            <test />
            <test id='myId'/>
            <test class='myClass'/>
            <test id='myId' class='myClass'/>
        </root>
        """
        result = self.skinner.skin(testSkin)
        (selector, declarations), = self.iterAuthor(result)

        testElemIF = getNested(result, 1).getCSSElement()
        self.assertEqual(selector.matches(testElemIF), False)

        testElemIF = getNested(result, 2).getCSSElement()
        self.assertEqual(selector.matches(testElemIF), False)

        testElemIF = getNested(result, 3).getCSSElement()
        self.assertEqual(selector.matches(testElemIF), False)

        testElemIF = getNested(result, 4).getCSSElement()
        self.assertEqual(selector.matches(testElemIF), True)

    def testAttr(self):
        testSkin = """<?xml version='1.0'?>
        <root>
            <style>test[attr]{value: 1}</style>

            <test />
            <test fun='attr'/>
            <test attr='fun'/>
        </root>
        """
        result = self.skinner.skin(testSkin)
        (selector, declarations), = self.iterAuthor(result)

        testElemIF = getNested(result, 1).getCSSElement()
        self.assertEqual(selector.matches(testElemIF), False)

        testElemIF = getNested(result, 2).getCSSElement()
        self.assertEqual(selector.matches(testElemIF), False)

        testElemIF = getNested(result, 3).getCSSElement()
        self.assertEqual(selector.matches(testElemIF), True)

    def testPseudo(self):
        testSkin = """<?xml version='1.0'?>
        <root>
            <style>test:first-child{value: 1}</style>

            <test />
            <test attr='fun'>
                <test fun='attr'/>
            </test>
        </root>
        """

        result = self.skinner.skin(testSkin)
        (selector, declarations), = self.iterAuthor(result)

        testElemIF = getNested(result, 1).getCSSElement()
        self.assertEqual(selector.matches(testElemIF), False)

        testElemIF = getNested(result, 2).getCSSElement()
        self.assertEqual(selector.matches(testElemIF), False)

        testElemIF = getNested(result, 2, 0).getCSSElement()
        self.assertEqual(selector.matches(testElemIF), True)

    def testCombinerDescendents(self):
        testSkin = """<?xml version='1.0'?>
        <root>
            <style>root test test{value: 1}</style>

            <test />
            <test attr='fun'>
                <test fun='attr'>
                    <test id='another'/>
                </test>
            </test>
        </root>
        """

        result = self.skinner.skin(testSkin)
        (selector, declarations), = self.iterAuthor(result)

        testElemIF = getNested(result, 1).getCSSElement()
        self.assertEqual(selector.matches(testElemIF), False)

        testElemIF = getNested(result, 2).getCSSElement()
        self.assertEqual(selector.matches(testElemIF), False)

        testElemIF = getNested(result, 2, 0).getCSSElement()
        self.assertEqual(selector.matches(testElemIF), True)

        testElemIF = getNested(result, 2, 0, 0).getCSSElement()
        self.assertEqual(selector.matches(testElemIF), True)

    def testCombinerChild(self):
        testSkin = """<?xml version='1.0'?>
        <root>
            <style>root>test>test{value: 1}</style>

            <test />
            <test attr='fun'>
                <test fun='attr'>
                    <test id='myId'/>
                </test>
            </test>
        </root>
        """

        result = self.skinner.skin(testSkin)
        (selector, declarations), = self.iterAuthor(result)

        testElemIF = getNested(result, 1).getCSSElement()
        self.assertEqual(selector.matches(testElemIF), False)

        testElemIF = getNested(result, 2).getCSSElement()
        self.assertEqual(selector.matches(testElemIF), False)

        testElemIF = getNested(result, 2, 0).getCSSElement()
        self.assertEqual(selector.matches(testElemIF), True)

        testElemIF = getNested(result, 2, 0, 0).getCSSElement()
        self.assertEqual(selector.matches(testElemIF), False)

    def testCombinerFollows(self):
        testSkin = """<?xml version='1.0'?>
        <root>
            <style>test+test{value: 1}</style>

            <test />
            <test attr='fun'>
                <test fun='attr'/>
                <test id='myId'/>
            </test>
            <test class='myClass'/>
        </root>
        """

        result = self.skinner.skin(testSkin)
        (selector, declarations), = self.iterAuthor(result)

        testElemIF = getNested(result, 1).getCSSElement()
        self.assertEqual(selector.matches(testElemIF), False)

        testElemIF = getNested(result, 2).getCSSElement()
        self.assertEqual(selector.matches(testElemIF), True)

        testElemIF = getNested(result, 2, 0).getCSSElement()
        self.assertEqual(selector.matches(testElemIF), False)

        testElemIF = getNested(result, 2, 1).getCSSElement()
        self.assertEqual(selector.matches(testElemIF), True)

        testElemIF = getNested(result, 3).getCSSElement()
        self.assertEqual(selector.matches(testElemIF), True)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Unittest Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    unittest.main()

