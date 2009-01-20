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

from pprint import pprint
import xml.dom.minidom
from TG.w3c import css, cssDOMElementInterface

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Constants / Variables / Etc. 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

stylesheet = """\
* {
    font-size: medium;
    bgcolor: orange;
    fgcolor: blue;
}

slideshow {
    bgcolor: black;
    fgcolor: white;
}

slideshow * {
    fgcolor: inherit;
    bgcolor: inherit;
}

slideshow > title {
    font-size: 80pt;
}

slide {
    image: url('page-image.png');
}

slide:last-child {
    fgcolor: yellow;
    image: url('last-page-image.png');
}

slide > title {
    font-size: 40pt;
}

point {
    font-size: medium;
}

point#special {
    font-size: xx-large;
    fgcolor: red;
    bgcolor: yellow;
}
"""

document = """\
<?xml version='1.0' ?>
<!-- Derived from 13.7.2 DOM Example of the Python 2.3 Documentation -->
<slideshow>
    <title>Demo slideshow combined with CSS</title>

    <slide>
        <title>Intro CSS Slide</title>
        <point>This is a CSS demo for xml.dom</point>
        <point>for processing slides with CSS!</point>
    </slide>

    <slide>
        <title>Another CSS demo slide</title>

        <point>It is important</point>
        <point>To have more than</point>
        <point>one slide</point>
    </slide>

    <slide>
        <title>Last CSS demo slide title</title>
        <point id='special'>Thanks for looking at CSS!</point>
    </slide>

</slideshow>
"""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def getCSSAttr(self, cssCascade, attrName, default=NotImplemented):
    if attrName in self.cssAttrs:
        return self.cssAttrs[attrName]

    result = None

    attrValue = self.attributes.get(attrName, None)
    if attrValue is not None:
        result = cssCascade.parser.parseSingleAttr(attrValue.value)

    if result is None:
        result = cssCascade.findStyleFor(self.cssElement, attrName, default)

        print
        print "SHANE:"
        for e in cssCascade.findAllCSSRulesFor(self.cssElement):
            print e
        print


    if result == 'inherit':
        if hasattr(self.parentNode, 'getCSSAttr'):
            result = self.parentNode.getCSSAttr(cssCascade, attrName, default)
        elif default is not NotImplemented:
            return default
        else:
            raise LookupError("Could not find inherited CSS attribute value for '%s'" % (attrName,))

    self.cssAttrs[attrName] = result
    return result
xml.dom.minidom.Element.getCSSAttr = getCSSAttr

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Demo
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# this is an informal schema that maps tag names to the css attributes they
# should have
tagToAttrNames = {
    'slideshow': 'fgcolor bgcolor'.split(),
    'title': 'font-size fgcolor bgcolor'.split(),
    'slide': 'image fgcolor bgcolor'.split(),
    'point': 'font-size fgcolor bgcolor'.split(),
    }

def visitElement(element, children, cssCascade):
    """Visits individual elements, and sets css attributes on them"""
    element.cssElement = cssDOMElementInterface.CSSDOMElementInterface(element)
    element.cssAttrs = {}
    element.cssElement.onCSSParserVisit(cssCascade.parser)

    cssAttrMap = {}
    for cssAttrName in tagToAttrNames.get(element.tagName, []):
        cssAttrMap[cssAttrName] = element.getCSSAttr(cssCascade, cssAttrName)

    result = ["%s: %r" % (element.tagName, cssAttrMap)]
    result.extend(["    " + r for line in children for r in line])
    return result

def visitElementNodes(root, visit=visitElement, **kw):
    """Visits all ELEMENT_NODEs of a dom recursively"""
    for node in root.childNodes:
        if node.nodeType == node.ELEMENT_NODE:
            children = visitElementNodes(node, visit, **kw)
            yield visit(node, children, **kw)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == "__main__":
    # parse the document into a dom
    dom = xml.dom.minidom.parseString(document)

    # parse the stylesheet
    cssParser = css.CSSParser()
    authorSS = cssParser.parse(stylesheet)
    # create the css cascade from the stylesheet
    cssCascade = css.CSSCascadeStrategy(authorSS)
    cssCascade.parser = cssParser

    # Visit all the nodes with the cssParser for inline styles and cssCascade for cssAttribute resolution
    slideshow = visitElementNodes(dom, cssCascade=cssCascade).next()
    slideshow = "    "+"\n    ".join(slideshow )

    # print our prepared result!
    print
    print
    print "Results of CSS attributed DOM:"
    print
    print slideshow
    print

