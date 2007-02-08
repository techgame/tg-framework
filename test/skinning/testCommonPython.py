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

from TG.skinning.engine import XMLSkinner, XMLSkin
from TG.skinning.common import skin as CommonSkin
from TG.skinning.common import python as PythonSkin

from TG.skinning.common.skin import compound
from TG.skinning.common.skin.skin import skin
from TG.skinning.common.skin.context import context
from TG.skinning.common.skin.ignore import ignore
from TG.skinning.common.skin.store import store, StoreXML

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def getNested(owner, *addrs):
    for addr in addrs:
        owner = owner.getChildren()[addr]
    return owner

class TestCommonPython(unittest.TestCase):
    def setUp(self):
        self.skinner = XMLSkinner().installSkins(CommonSkin, PythonSkin)
    def tearDown(self):
        del self.skinner

    def testInline(self):
        testSkin = XMLSkin("""<?xml version='1.0'?>
            <skin xmlns:py='TG.skinning.common.python' xmlns='TG.skinning.common.skin'>
                <py:inline>
                    step1 = elem.step1 = True
                    <context/>
                    step2 = elem.step2 = 42
                    <skin/>
                    step3 = elem.step3 = 'here'

                    assert step1 == True
                    assert step2 == 42
                    assert step3 == 'here'
                </py:inline>
            </skin>
            """)
        result = self.skinner.skin(testSkin)

        self.assertEqual(type(result), skin)
        self.assertEqual(len(result.getChildren()), 2)

        self.assertEqual(result.step1, True)
        self.assertEqual(type(getNested(result, 0)), context)
        self.assertEqual(result.step2, 42)
        self.assertEqual(type(getNested(result, 1)), skin)
        self.assertEqual(result.step3, 'here')

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testTryList(self):
        testSkin = XMLSkin("""<?xml version='1.0'?>
            <skin xmlns:py='TG.skinning.common.python' xmlns='TG.skinning.common.skin'>
                <py:trylist>
                    <elementDoesNotExist>
                        <subElementDoesNotExist/>
                        <nsDoesNotExist xmlns='namespace does not exist'/>
                    </elementDoesNotExist>
                    <skin>
                        <subElementDoesNotExist/>
                        <nsDoesNotExist xmlns='namespace does not exist'/>
                    </skin>
                    <context>
                        <ignore/>
                        <store/>
                    </context>
                    <elementDoesNotExist>
                        <subElementDoesNotExist/>
                        <nsDoesNotExist xmlns='namespace does not exist'/>
                    </elementDoesNotExist>
                    <skin>
                        <section name='stuff'/>
                        <ignore/>
                    </skin>
                </py:trylist>
            </skin>
            """)
        result = self.skinner.skin(testSkin)

        self.assertEqual(len(result.getChildren()), 1)
        self.assertEqual(type(result), skin)
        self.assertEqual(type(getNested(result, 0)), context)
        self.assertEqual(type(getNested(result, 0, 0)), ignore)
        self.assertEqual(type(getNested(result, 0, 1)), store)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testInlineExtended(self):
        testSkin = XMLSkin("""<?xml version='1.0'?>
            <skin xmlns:py='TG.skinning.common.python' xmlns='TG.skinning.common.skin'>
                <py:inline>
                    def myTest():
                        assert elem.__class__.__name__ == 'skin'
                    myTest()
                </py:inline>
            </skin>
            """)
        result = self.skinner.skin(testSkin)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Unittest Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    unittest.main()


