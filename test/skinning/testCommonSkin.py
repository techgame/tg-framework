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

class TestCommonSkin(unittest.TestCase):
    def setUp(self):
        self.skinner = XMLSkinner().installSkins(CommonSkin)

    def tearDown(self):
        del self.skinner

    def testSkinElement(self):
        testSkin = XMLSkin("""<?xml version='1.0'?>
            <skin xmlns="TG.skinning.common.skin" />""")
        result = self.skinner.skin(testSkin)
        self.assertEqual(type(result), skin)
    
    def testIgnoreElement(self):
        testSkin = XMLSkin("""<?xml version='1.0'?>
            <ignore xmlns="TG.skinning.common.skin">
                <elementDoesNotExist>
                    <subElementDoesNotExist/>
                    <nsDoesNotExist xmlns='namespace does not exist'/>
                </elementDoesNotExist>
            </ignore>""")
        result = self.skinner.skin(testSkin)
        self.assertEqual(type(result), ignore)
        self.assertEqual(vars(result), {})

    def testStore(self):
        testSkin = XMLSkin("""<?xml version='1.0'?>
            <store xmlns="TG.skinning.common.skin">
                <elementDoesNotExist>
                    <subElementDoesNotExist/>
                    <nsDoesNotExist xmlns='namespace does not exist'/>
                </elementDoesNotExist>
            </store>""")
        result = self.skinner.skin(testSkin)

        self.assertEqual(type(result), store)

    def testSection(self):
        testSkin = XMLSkin("""<?xml version='1.0'?>
            <section name='test' xmlns="TG.skinning.common.skin">
                <elementDoesNotExist>
                    <subElementDoesNotExist/>
                    <nsDoesNotExist xmlns='namespace does not exist'/>
                </elementDoesNotExist>
            </section>""")
        result = self.skinner.skin(testSkin)

        self.assertEqual(type(result), section)

    def testTemplate(self):
        testSkin = XMLSkin("""<?xml version='1.0'?>
            <skin xmlns="TG.skinning.common.skin">
                <section name='mySection'>
                    <context>
                        <store/>    
                    </context>
                </section>
                <template name='myTemplate'>
                    <skin>
                        <ignore/>
                        <template expand='myTemplate' />
                        <ignore/>
                        <template invoke='mySection' />
                        <ignore/>
                    </skin>
                </template>

                <template invoke='myTemplate'>
                    <context />
                    <skin />
                </template>
                <template invoke='mySection'>
                    <context />
                    <skin />
                </template>
            </skin>""")
        result = self.skinner.skin(testSkin)

        self.assertEqual(type(result), skin)
        self.assertEqual(len(result.getChildren()), 4)

        self.assertEqual(type(getNested(result, 0)), section)

        self.assertEqual(type(getNested(result, 1)), template)

        self.assertEqual(type(getNested(result, 2)), skin)
        self.assertEqual(len(getNested(result, 2).getChildren()), 6)
        self.assertEqual(type(getNested(result, 2, 0)), ignore)
        self.assertEqual(type(getNested(result, 2, 1)), context)
        self.assertEqual(type(getNested(result, 2, 2)), skin)
        self.assertEqual(type(getNested(result, 2, 3)), ignore)
        self.assertEqual(type(getNested(result, 2, 4)), context)
        self.assertEqual(type(getNested(result, 2, 4, 0)), store)
        self.assertEqual(type(getNested(result, 2, 5)), ignore)

        self.assertEqual(type(getNested(result, 3)), context)
        self.assertEqual(type(getNested(result, 3, 0)), store)
        self.assertEqual(len(getNested(result, 3).getChildren()), 1)

    def testReference(self):
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

