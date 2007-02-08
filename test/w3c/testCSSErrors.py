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
import sys

from TG.w3c import css

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TestCSSErrors(unittest.TestCase):
    def setUp(self):
        self.parserStrict = css.CSSParser()
        self.parserStrict.bParseStrict = True
        self.parserTolerant = css.CSSParser()
    def tearDown(self):
        del self.parserStrict
        del self.parserTolerant

    def parseCSS(self, testcss, errortext):
        result = self.parseStrictCSS(testcss, errortext)
        result = self.parseTolerantCSS(testcss, errortext)
        return result

    def parseStrictCSS(self, testcss, errortext):
        try: 
            result = self.parserStrict.parse(testcss)
        except css.CSSParseError: 
            result = None
        else: 
            self.fail('Should fail strict test: ' + errortext)
        return result
    
    def parseTolerantCSS(self, testcss, errortext):
        try: 
            result = self.parserTolerant.parse(testcss)
        except css.CSSParseError: 
            raise
            self.fail('Should NOT fail tolerant test: ' + errortext)
        return result

    def testMissingColon(self):
        self.parseCSS('p { color:green; color } ', 'Malformed declaration missing \':\' and value')
        self.parseCSS('p { color:green; color orange} ', 'Malformed declaration missing \':\' and value')
        self.parseCSS('p { color:red;   color; color:green }', 'Malformed declaration missing \':\' with expected recovery')
        self.parseCSS('p { color:red;   color orange; color:green }', 'Malformed declaration missing \':\' with expected recovery')

    def testMissingValue(self):
        self.parseCSS('p { color:green; color: }', 'Malformed declaration missing value at end of construct')
        self.parseCSS('p { color:red;   color:; color:green }', 'Malformed declaration missing value in the middle of construct')

    def testUnexpectedBlock(self):
        self.parseCSS('p { color:green; color{;color:maroon} }', 'Unexpected tokens { }')
        self.parseCSS('p { color:red;   color{;color:maroon}; color:green }', 'Unexpected tokens {} with recovery')
     
    def testInvalidAtKeywords(self):
        self.parseCSS('''@two-dee blah blah blah;''', '''@two-dee should be ignored''')
        self.parseCSS('''
            @three-dee {
                @background-lighting {
                    azimuth: 30deg;
                    elevation: 190deg;
                }
                h1 { color: red }
            }
            h1 { color: blue }
            ''', '@three-dee should be ignored')
        self.parseCSS('''
            @three-dee 
                @background-lighting {
                    azimuth: 30deg;
                    elevation: 190deg;
                }
                h1 { color: red }
            }
            h1 { color: blue }
            ''', '@three-dee should be ignored even though it is missing a start bracket')
    
    def testUnexpectedEndOfStylesheet(self):
        self.parseCSS('''
            p { content: 'Hello'
            ''', 'Should parse as if all open constructs were closed')
        self.parseCSS('''
            h1 { content: 'Hello
            ''', 'Should parse as if all open constructs were closed')
        self.parseCSS('''
            @media screen {
                p:before { content: 'Hello
            ''', 'Should parse as if all open constructs were closed')
        self.parseCSS('''
            @media screen {
                p:before { content: 'Hello'
            ''', 'Should parse as if all open constructs were closed')
    
    def testUnexpectedEndOfString(self):
        self.parseCSS('''
            p {
                color: green;
                font-family: 'Courier New Times            
                color: red;
                color: green;
                }
            ''', 'Should skip open string value')
        self.parseCSS('''
            p {
                color: green;
                font-family: 'Courier New Times            
                color: red;
                color: green;
                }
            ''', 'Should skip open string value')

    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Unittest Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    unittest.main()

