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
import unittest

from TG.common import path
from TG.w3c import css

import wx
from TG.guiTools.wx.cssFont import CSSFont

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ wxApp required
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if not wx.GetApp():
    app = wx.PySimpleApp()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TestCSSFontInline(unittest.TestCase):
    """This is mostly a test through exercise of the API, not through test of the results"""

    _output = None

    def setUp(self):
        self.parseInline = css.CSSParser().parseInline

    def write(self, text):
        if self._output:
            self._output.write(text)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Tests
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testFontFamily(self):
        print >> self
        print >> self, "font-family"
        print >> self, "-----------"
        css ="""font-family: Gill, Helvetica, sans-serif"""
        values = self.parseInline(css)
        print >> self, "   ", repr(css)
        print >> self, "   ", (CSSFont.cssFamilies(values['font-family']))
        print >> self

        css = """font-family: "Courier New", serif"""
        values = self.parseInline(css)
        print >> self, "   ", repr(css)
        print >> self, "   ", (CSSFont.cssFamilies(values['font-family']))
        print >> self

    def testFontStyle(self):
        print >> self
        print >> self, "font-style"
        print >> self, "----------"
        css = """font-style: italic"""
        values = self.parseInline(css)
        print >> self, "   ", repr(css)
        print >> self, "   ", (CSSFont.cssStyle(values['font-style']))
        print >> self

        css = """font-style: normal"""
        values = self.parseInline(css)
        print >> self, "   ", repr(css)
        print >> self, "   ", (CSSFont.cssStyle(values['font-style']))
        print >> self

    def testFontVariant(self):
        print >> self
        print >> self, "font-variant"
        print >> self, "------------"
        css = """font-variant: smal-caps"""
        values = self.parseInline(css)
        print >> self, "   ", repr(css)
        print >> self, "   ", (CSSFont.cssVariant(values['font-variant']))
        print >> self

        css = """font-variant: normal"""
        values = self.parseInline(css)
        print >> self, "   ", repr(css)
        print >> self, "   ", (CSSFont.cssVariant(values['font-variant']))
        print >> self

        css = """font-variant: oblique"""
        values = self.parseInline(css)
        print >> self, "   ", repr(css)
        print >> self, "   ", (CSSFont.cssVariant(values['font-variant']))
        print >> self

    def testFontWeight(self):
        print >> self
        print >> self, "font-weight"
        print >> self, "-----------"
        css = """font-weight: bold"""
        values = self.parseInline(css)
        print >> self, "   ", repr(css)
        print >> self, "   ", (CSSFont.cssWeight(values['font-weight']))
        print >> self

        css = """font-weight: 600"""
        values = self.parseInline(css)
        print >> self, "   ", repr(css)
        print >> self, "   ", (CSSFont.cssWeight(values['font-weight']))
        print >> self

        css = """font-weight: lighter"""
        values = self.parseInline(css)
        print >> self, "   ", repr(css)
        print >> self, "   ", (CSSFont.cssWeight(values['font-weight']))
        print >> self

    def testFontSize(self):
        print >> self
        print >> self, "font-size"
        print >> self, "---------"
        css = """font-size: xx-small"""
        values = self.parseInline(css)
        print >> self, "   ", repr(css)
        print >> self, "   ", (CSSFont.cssSize(values['font-size']))
        print >> self

        css = """font-size: larger"""
        values = self.parseInline(css)
        print >> self, "   ", repr(css)
        print >> self, "   ", (CSSFont.cssSize(values['font-size']))
        print >> self

        css = """font-size: smaller"""
        values = self.parseInline(css)
        print >> self, "   ", repr(css)
        print >> self, "   ", (CSSFont.cssSize(values['font-size']))
        print >> self

        css = """font-size: 12"""
        values = self.parseInline(css)
        print >> self, "   ", repr(css)
        print >> self, "   ", (CSSFont.cssSize(values['font-size']))
        print >> self

        css = """font-size: 12pt"""
        values = self.parseInline(css)
        print >> self, "   ", repr(css)
        print >> self, "   ", (CSSFont.cssSize(values['font-size']))
        print >> self

        css = """font-size: 80%"""
        values = self.parseInline(css)
        print >> self, "   ", repr(css)
        print >> self, "   ", (CSSFont.cssSize(values['font-size']))
        print >> self

        css = """font-size: 2em"""
        values = self.parseInline(css)
        print >> self, "   ", repr(css)
        print >> self, "   ", (CSSFont.cssSize(values['font-size']))
        print >> self

    def testFont(self):
        print >> self
        print >> self, "font"
        print >> self, "----"
        css = """font: 12px/14px sans-serif"""
        values = self.parseInline(css)
        print >> self, "   ", repr(css)
        print >> self, "   ", (CSSFont.cssFont(values['font']))
        print >> self

        css = """font: 80% sans-serif"""
        values = self.parseInline(css)
        print >> self, "   ", repr(css)
        print >> self, "   ", (CSSFont.cssFont(values['font']))
        print >> self

        css = """font: x-large/110% "Courier New", serif"""
        values = self.parseInline(css)
        print >> self, "   ", repr(css)
        print >> self, "   ", (CSSFont.cssFont(values['font']))
        print >> self

        css = """font: bold italic large Tahoma, serif"""
        values = self.parseInline(css)
        print >> self, "   ", repr(css)
        print >> self, "   ", (CSSFont.cssFont(values['font']))
        print >> self

        css = """font: normal small-caps 120%/120% fantasy"""
        values = self.parseInline(css)
        print >> self, "   ", repr(css)
        print >> self, "   ", (CSSFont.cssFont(values['font']))
        print >> self

    def testFontFromCSS(self):
        print >> self
        print >> self, "Font from CSS"
        print >> self, "-------------"
        css = """font: 12px/14px sans-serif"""
        values = self.parseInline(css)
        print >> self, "   ", repr(css)
        print >> self, "   ", CSSFont.fromCSS(values)
        print >> self

        css = """font: 80% sans-serif"""
        values = self.parseInline(css)
        print >> self, "   ", repr(css)
        print >> self, "   ", CSSFont.fromCSSFont(values['font'])
        print >> self

        css = """font: x-large/110% "Courier New", serif"""
        values = self.parseInline(css)
        print >> self, "   ", repr(css)
        print >> self, "   ", CSSFont.fromCSS(values)
        print >> self

        css = """font: bold italic large Tahoma, serif"""
        values = self.parseInline(css)
        print >> self, "   ", repr(css)
        print >> self, "   ", CSSFont.fromCSSFont(values['font'])
        print >> self

        css = """font: normal small-caps 120%/120% fantasy"""
        values = self.parseInline(css)
        print >> self, "   ", repr(css)
        print >> self, "   ", CSSFont.fromCSSFont(values['font'])
        print >> self

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Unittest Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    TestCSSFontInline._output = sys.stdout
    unittest.main()

