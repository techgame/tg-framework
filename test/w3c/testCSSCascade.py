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
import xml.dom.minidom
from TG.w3c import css, cssDOMElementInterface

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Constants / Variables / Etc. 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

document = """<?xml version='1.0' ?>
<body>
    <h1>First</h1>
    <h2>Second</h2>
</body>
"""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def getCSSAttr(self, cssCascade, attrName, default=NotImplemented):
    """We attach this method to xml.dom.minidom.Element"""
    if attrName in self.cssAttrs:
        return self.cssAttrs[attrName]

    result = None

    attrValue = self.attributes.get(attrName, None)
    if attrValue is not None:
        result = cssCascade.parser.parseSingleAttr(attrValue.value)

    if result is None:
        result = cssCascade.findStyleFor(self.cssElement, attrName, default)

    if result == 'inherit':
        if hasattr(self.parentNode, 'getCSSAttr'):
            result = self.parentNode.getCSSAttr(cssCascade, attrName, default)
        elif default is not NotImplemented:
            return default
        else:
            raise LookupError("Could not find inherited CSS attribute value for '%s'" % (attrName,))

    self.cssAttrs[attrName] = result
    return result

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Setup code derived from a demo
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# this is an informal schema that maps tag names to the css attributes they
# should have
tagToAttrNames = {
    'h1': 'color align'.split(),
    'h2': 'color align'.split(),
    }

def visitElement(element, children, cssCascade):
    """Visits individual elements, and sets css attributes on them"""
    element.cssElement = cssDOMElementInterface.CSSDOMElementInterface(element)
    element.cssAttrs = {}

    cssAttrMap = {}
    for cssAttrName in tagToAttrNames.get(element.tagName, []):
        cssAttrMap[cssAttrName] = element.getCSSAttr(cssCascade, cssAttrName)

    return (element.tagName, cssAttrMap, list(children))

def visitElementNodes(root, visit=visitElement, **kw):
    """Visits all ELEMENT_NODEs of a dom recursively"""
    for node in root.childNodes:
        if node.nodeType == node.ELEMENT_NODE:
            children = visitElementNodes(node, visit, **kw)
            yield visit(node, children, **kw)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Unittest
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TestCSSWithMinidom(unittest.TestCase):
    def setUp(self):
        # parse the document into a dom
        self.dom = xml.dom.minidom.parseString(document)

        # parse the stylesheet
        self.cssParser = css.CSSParser()
        # create the css cascade from the stylesheet
        self.cssCascade = css.CSSCascadeStrategy()
        self.cssCascade.parser = self.cssParser

        xml.dom.minidom.Element.getCSSAttr = getCSSAttr

    def tearDown(self):
        del xml.dom.minidom.Element.getCSSAttr

    def css(self, **kw):
        for cssOrigin, stylesheet in kw.iteritems():
            setattr(self.cssCascade, cssOrigin, self.cssParser.parse(stylesheet))
        return self.cssCascade

    def test_UserAgent_Author(self):
        css = self.css( 
                userAgent='h1 { align: left; color: red } h2 { align: right; color: orange !important}',
                author='h1 { align: right; color: green } h2 { align: left !important; color: blue}')

        result = visitElementNodes(self.dom, cssCascade=css).next()
        headings = result[-1]
        self.assertEqual(result[0], 'body')
        self.assertEqual(headings[0], (u'h1', {'align': 'right', 'color': 'green'}, []))
        self.assertEqual(headings[1], (u'h2', {'align': 'left', 'color': 'blue'}, []))

    def test_Author_User(self):
        css = self.css( 
                author='h1 { align: left; color: red } h2 { align: right; color: orange !important}',
                user='h1 { align: right; color: green } h2 { align: left !important; color: blue }')

        result = visitElementNodes(self.dom, cssCascade=css).next()
        headings = result[-1]
        self.assertEqual(result[0], 'body')
        self.assertEqual(headings[0], (u'h1', {'align': 'left', 'color': 'red'}, []))
        self.assertEqual(headings[1], (u'h2', {'align': 'left', 'color': 'orange'}, []))

    def test_UserAgent_User(self):
        css = self.css( 
                userAgent='h1 { align: left; color: red } h2 { align: right; color: orange !important}',
                user='h1 { align: right; color: green } h2 { align: left !important; color: blue }')

        result = visitElementNodes(self.dom, cssCascade=css).next()
        headings = result[-1]
        self.assertEqual(result[0], 'body')
        self.assertEqual(headings[0], (u'h1', {'align': 'right', 'color': 'green'}, []))
        self.assertEqual(headings[1], (u'h2', {'align': 'left', 'color': 'blue'}, []))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Unittest Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    unittest.main()

