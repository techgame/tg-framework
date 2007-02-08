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

from TG.skinning.common.skin import compound
from TG.skinning.common.skin.skin import skin
from TG.skinning.common.skin.context import context
from TG.skinning.common.skin.ignore import ignore
from TG.skinning.common.skin.store import store, StoreXML

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MyComponentModel(compound.CompoundModelBase):
    initializeCalled = False
    finalizeCalled = False

    def onSkinInitialize(self, element, elemBuilder):
        self.initializeCalled = True
    
    def onSkinFinalize(self, element, elemBuilder):
        self.finalizeCalled = True

class MyComponentElement(compound.UnifiedCompoundElement):
    CompoundModelFactory = MyComponentModel
    xmlSkin = XMLSkin("""<?xml version='1.0'?>
        <context>
            <store/>
            <template expand='::contents'/>
            <store/>
        </context>
        """)

def installMyComponentElement(builder):
    builder.xmlFactories[('TG.skinning.common.skin', 'myComponent')] = lambda *args: MyComponentElement

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def getNested(owner, *addrs):
    for addr in addrs:
        owner = owner.getChildren()[addr]
    return owner

class TestCommonSkinCompound(unittest.TestCase):
    def setUp(self):
        self.skinner = XMLSkinner().installSkins(CommonSkin)
        self.skinner.installSkins(installMyComponentElement)

    def tearDown(self):
        del self.skinner

    def test(self):
        testSkin = XMLSkin("""<?xml version='1.0'?>
            <skin xmlns='TG.skinning.common.skin'>
                <myComponent>
                    <ignore />
                    <context/>
                </myComponent>
            </skin>
            """)
        result = self.skinner.skin(testSkin)
        self.assertEqual(type(result), skin)

        self.assertEqual(len(result.getChildren()), 1)
        self.assertEqual(type(getNested(result, 0)), MyComponentElement)
        elem = getNested(result, 0)
        self.assert_(elem.getObject() is not None)
        self.assert_(elem.getObject().initializeCalled)
        self.assert_(elem.getObject().finalizeCalled)

        self.assertEqual(len(getNested(result, 0).getChildren()), 1)
        self.assertEqual(type(getNested(result, 0)), MyComponentElement)

        self.assertEqual(type(getNested(result, 0, 0)), context)
        self.assertEqual(len(getNested(result, 0, 0).getChildren()), 4)
        self.assertEqual(type(getNested(result, 0, 0, 0)), store)
        self.assertEqual(type(getNested(result, 0, 0, 1)), ignore)
        self.assertEqual(type(getNested(result, 0, 0, 2)), context)
        self.assertEqual(type(getNested(result, 0, 0, 3)), store)
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Unittest Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    unittest.main()


