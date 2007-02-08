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
        authorSS = result.ctx.getCSSCascade().authorSS
        return authorSS[0].items()

    def testOverall(self):
        testSkin = """<?xml version='1.0'?>
        <root stuff='Yep'>
            <style>test {value: 1; other: 'not 42'; stuff: inherit}</style>
            <test other='42'/>
            <test id='myId' other='42'/>
            <test class='myClass' other='42'/>
            <test class='myClass myOtherClass' other='42'/>
            <test id='myId' class='myClass' other='42'/>
        </root>
        """
        result = self.skinner.skin(testSkin)
        self.assertEqual(type(result), root)
        self.assertEqual(type(getNested(result, 0)), style)

        for testNode in result.getChildren()[1:]:
            self.assertEqual(testNode.getStyleSetting('value'), '1')
            self.assertRaises(LookupError, testNode.getSetting, 'value')
            self.assertRaises(LookupError, testNode.getStyleSetting, 'does not exist')
            self.assertEqual(testNode.getStyleSetting('other'), '42')
            self.assertEqual(testNode.getStyleSetting('stuff'), 'Yep')
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Unittest Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    unittest.main()

