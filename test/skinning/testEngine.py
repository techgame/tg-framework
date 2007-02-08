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
import StringIO

from TG.skinning.engine import XMLSkinner, XMLSkin
from TG.skinning.common import skin as CommonSkin
from TG.skinning.common import python as PythonSkin

from TG.skinning.common.skin.context import context
from TG.skinning.common.skin.ignore import ignore
from TG.skinning.common.skin.reference import reference
from TG.skinning.common.skin.section import section
from TG.skinning.common.skin.skin import skin
from TG.skinning.common.skin.store import store, StoreXML
from TG.skinning.common.skin.template import template

from TG.uriResolver.fileobj.generic import GenericResolver

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def getNested(owner, *addrs):
    for addr in addrs:
        owner = owner.getChildren()[addr]
    return owner

class TestEngine(unittest.TestCase):
    def setUp(self):
        self.skinner = XMLSkinner().installSkins(CommonSkin, PythonSkin)

    def tearDown(self):
        del self.skinner

    def testSkinElement(self):
        """Test Skin Element uses skin()"""
        testSkin = XMLSkin("""<?xml version='1.0'?>
            <skin xmlns="TG.skinning.common.skin" />""")
        result = self.skinner.skin(testSkin)
        self.assertEqual(type(result), skin)
        self.assertEqual(len(result.getChildren()), 0)
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testGraftElement(self):
        """Test Graft Element uses graftSkin()"""
        testSkin = XMLSkin("""<?xml version='1.0'?>
            <skin xmlns="TG.skinning.common.skin" />""")

        result = self.skinner.skin(testSkin)
        graftElem = result

        self.assertEqual(type(graftElem), skin)
        self.assertEqual(len(graftElem.getChildren()), 0)

        #~ now graft in the following skin ~~~~~~~~~~~~~~~~~~
        testSkin = XMLSkin("""<?xml version='1.0'?>
            <context name='mySection' xmlns="TG.skinning.common.skin" >
                <skin>
                    <store/>    
                </skin>
                <ignore/>
            </context>
            """)

        result = self.skinner.graftSkin(testSkin, graftElem)

        self.assertEqual(type(graftElem), skin)
        self.assertEqual(len(graftElem.getChildren()), 1)

        self.assertEqual(type(result), context)
        self.assertEqual(len(result.getChildren()), 2)

        self.assertEqual(type(getNested(result, 0)), skin)
        self.assertEqual(type(getNested(result, 0, 0)), store)

        self.assertEqual(type(getNested(graftElem, 0, 0)), skin)
        self.assertEqual(type(getNested(graftElem, 0, 0, 0)), store)

        self.assertEqual(type(getNested(result, 1)), ignore)
        self.assertEqual(type(getNested(graftElem, 0, 1)), ignore)


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testReference(self):
        """Test Reference uses skinFromStack() via the reference element"""
        class Resolver(GenericResolver):
            testFileA = XMLSkin("""<?xml version='1.0'?>
                <context>
                    <ignore/>
                    <store/>
                </context>""")
            testFileB = XMLSkin("""<?xml version='1.0'?>
                <skin xmlns="TG.skinning.common.skin">
                    <context/>
                </skin>""")

            def setNodeData(self, node):
                node.setPath(__file__)

                testFile = getattr(self, node.getSubPath(), None)
                if testFile:
                    node.setData(testFile.getSource())
                else:
                    node.setData(None)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        testSkin = XMLSkin("""<?xml version='1.0'?>
            <skin xmlns="TG.skinning.common.skin">
                <reference ref='testFileA'/>
                <reference fromctx='testStringA' />
            </skin>
            """, Resolver())

        testStringA = XMLSkin("""<?xml version='1.0'?><store/>""")

        result = self.skinner.skin(testSkin, testStringA=testStringA)

        self.assertEqual(len(result.getChildren()), 2)
        self.assertEqual(type(result), skin)
        self.assertEqual(type(getNested(result, 0)), context)
        self.assertEqual(type(getNested(result, 0, 0)), ignore)
        self.assertEqual(type(getNested(result, 0, 1)), store)
        self.assertEqual(type(getNested(result, 1)), store)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Unittest Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    unittest.main()

