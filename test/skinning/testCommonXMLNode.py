#!/usr/bin/env python ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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
from TG.skinning.common import xmlNode

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TestCommonPython(unittest.TestCase):

    def testNoNamespace(self):
        testSkin = """<?xml version='1.0'?>
            <nodeA attr1='A.One' attr2="A.Two">
                <nodeB/>
                <nodeC attr1='C.One' attr2='C.Two'>
                    <nodeD>
                        Node D's text
                    </nodeD>
                </nodeC>
            </nodeA>
        """
        node = xmlNode.XMLNodeSkinner().skin(testSkin)
        self.assertEqual(node.node, 'nodeA')
        self.assertEqual(node.namespace, None)
        self.assertEqual(node.attrs, {'attr2': 'A.Two', 'attr1': 'A.One'})
        self.assertEqual(len(node), 5)
        self.assertEqual(len(node.listNodes()), 2)
        self.assertEqual([subnode.node for subnode in node.iterNodes()], ['nodeB', 'nodeC'])
        self.assertEqual([subnode.node for subnode in node['nodeC',][0].iterNodes()], ['nodeD'])
    
    def testNamespace(self):
        testSkin = """<?xml version='1.0'?>
            <nodeA xmlns='TG.skinning.common.xmlNode' attr1='A.One' attr2="A.Two">
                <nodeB/>
                <nodeC attr1='C.One' attr2='C.Two'>
                    <nodeD>
                        Node D's text
                    </nodeD>
                </nodeC>
            </nodeA>
        """
        skinner = XMLSkinner().installSkins(xmlNode)
        node = skinner.skin(testSkin)

        self.assertEqual(node.node, 'nodeA')
        self.assertEqual(node.namespace, 'TG.skinning.common.xmlNode')
        self.assertEqual(node.attrs, {'attr2': 'A.Two', 'attr1': 'A.One'})
        self.assertEqual(len(node), 5)
        self.assertEqual(len(node.listNodes()), 2)
        self.assertEqual([subnode.node for subnode in node.iterNodes()], ['nodeB', 'nodeC'])
        self.assertEqual([subnode.node for subnode in node['nodeC',][0].iterNodes()], ['nodeD'])
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Unittest Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    unittest.main()


