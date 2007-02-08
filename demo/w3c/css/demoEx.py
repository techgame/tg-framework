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

import sys
from pprint import pprint
import xml.dom.minidom

from TG.w3c import css, cssDOMElementInterface

import demo

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == "__main__":
    print 'Usage: demoEx.py <style.css> <slideshow.xml>'
    print

    print
    cssFilename = ''.join(sys.argv[1:2]) or 'style.css'
    cssFile = open(cssFilename, 'r')
    xmlFilename = ''.join(sys.argv[2:3]) or 'slideshow.xml'
    xmlFile = open(xmlFilename, 'r')

    # parse the stylesheet
    cssParser = css.CSSParser()
    print "Parsing \"%s\" using TG.w3c.css..." % (cssFilename,)
    authorSS = cssParser.parseFile(cssFile)

    # create the css cascade from the stylesheet
    cssCascade = css.CSSCascadeStrategy(authorSS)
    cssCascade.parser = cssParser

    print "Parsing \"%s\" using xml.dom.minidom..." % (xmlFilename,)
    # parse the document into a dom
    dom = xml.dom.minidom.parse(xmlFile)

    print "Applying the CSS Cascade to the XML DOM..."
    # Visit all the nodes with the cssParser for inline styles and cssCascade for cssAttribute resolution
    slideshow = demo.visitElementNodes(dom, cssCascade=cssCascade).next()
    slideshow = "    "+"\n    ".join(slideshow )

    # print our prepared result!
    print
    print
    print "Results of CSS attributed DOM:"
    print
    print slideshow
    print

