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

from TG.common import path
from TG.w3c import xmlNode

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TestCommonPython(unittest.TestCase):

    def testNoNamespace(self):
        testxml = """<?xml version='1.0'?>
            <nodeA attr1='A.One' attr2="A.Two">
                <nodeB/>
                <nodeC attr1='C.One' attr2='C.Two'>
                    <nodeD>
                        Node D's text
                    </nodeD>
                </nodeC>
            </nodeA>
        """
        node = xmlNode.Producer().parse(testxml)
        self.assertEqual(node.node, 'nodeA')
        self.assertEqual(node.namespace, None)
        self.assertEqual(node.attrs, {'attr2': 'A.Two', 'attr1': 'A.One'})
        self.assertEqual(len(node), 5)
        self.assertEqual(len(node.listNodes()), 2)
        self.assertEqual([subnode.node for subnode in node.iterNodes()], ['nodeB', 'nodeC'])
        self.assertEqual([subnode.node for subnode in node['nodeC',][0].iterNodes()], ['nodeD'])
    
    def testNamespace(self):
        testxml = """<?xml version='1.0'?>
            <nodeA xmlns='A Test Namespace' attr1='A.One' attr2="A.Two">
                <nodeB/>
                <nodeC attr1='C.One' attr2='C.Two'>
                    <nodeD>
                        Node D's text
                    </nodeD>
                </nodeC>
            </nodeA>
        """
        node = xmlNode.Producer().parse(testxml)
        self.assertEqual(node.node, 'nodeA')
        self.assertEqual(node.namespace, 'A Test Namespace')
        self.assertEqual(node.attrs, {'attr2': 'A.Two', 'attr1': 'A.One'})
        self.assertEqual(len(node), 5)
        self.assertEqual(len(node.listNodes()), 2)
        self.assertEqual([subnode.node for subnode in node.iterNodes()], ['nodeB', 'nodeC'])
        self.assertEqual([subnode.node for subnode in node['nodeC',][0].iterNodes()], ['nodeD'])

    def testBuilding(self):
        root = xmlNode.XMLNode('root', 'MyRootNamespace')
        root += 'Some cdata'
        root += ('subelem',)
        root += 'More data'
        root += ('element',)
        root += 'anotherelem', 'SubNamespace'
        anotherelem = root[-1]
        anotherelem.attrs['myattr'] = 'a value'
        anotherelem += 'some text'

        result = \
'''<root xmlns="MyRootNamespace">
    Some cdata
    <subelem/>
    More data
    <element/>
    <anotherelem xmlns="SubNamespace" myattr="a value">
        some text
    </anotherelem>
</root>'''
        self.assertEqual(result, root.toXML(True))

        result = '''<root xmlns="MyRootNamespace">Some cdata<subelem/>More data<element/><anotherelem xmlns="SubNamespace" myattr="a value">some text</anotherelem></root>'''
        self.assertEqual(result, root.toXML())
        self.assertEqual(root.toXML(False), root.toXML())
        

    def testJabberXMLFile(self):
        rootPath = path.path(__file__).parent.joinpath('media/JabberTest.xml')
        root = xmlNode.Producer().parseFile(rootPath.open())

        for data in root.iterData():
            self.assert_(data.strip() in ['SENT:', 'RECV:', ''])

        for node in root.iterNodes():
            self.assert_(node.node in ['iq', 'presence', 'message'], '%r\'s name was not iq, message, or presenece'%node)
            self.assertEqual(node.namespace, 'jabber:client', '%r\'s namespace was not \'jabber:client\''%node)
        
        self.assertEqual(len(root.listNodes('iq')), 10)
        self.assertEqual(len(root.listNodes('message')), 2)
        self.assertEqual(len(root.listNodes('presence')), 3)
        self.assertEqual(len(root.listNodes('query')), 0)
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Unittest Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    unittest.main()


