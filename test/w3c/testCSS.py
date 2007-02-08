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

class TestCSSInlineAttribute(unittest.TestCase):
    def setUp(self):
        self.parser = css.CSSParser()

    def assertCSSAttrValueEqual(self, good, equalfn=None, **kwAttributes):
        if equalfn is None: 
            equalfn = self.assertEqual
        fn = lambda r, v: equalfn(r['value'], v)
        self.assertCSSAttrEqual(good, fn, **kwAttributes)

    def assertCSSAttrEqual(self, good, equalfn=None, **kwAttributes):
        if equalfn is None:
            equalfn = self.assertEqual
        result = self.parser.parseAttributes(kwAttributes)
        equalfn(result, good)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Tests
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testOneValue(self):
        result = {'one':'1'}
        self.assertCSSAttrEqual(result, one='1')

    def testMultipleValue(self):
        result = {'one':'1', 'two':'2', 'three':'3'}
        self.assertCSSAttrEqual(result, one='1', two='2', three='3')

    def testListValue(self):
        result = ['1','2','3','4','5']
        self.assertCSSAttrValueEqual(result, value='1, 2, 3, 4, 5,')

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testIdent(self):
        self.assertCSSAttrValueEqual('anIdent', value='anIdent')
        self.assertCSSAttrValueEqual('anIdent-with-dashes', value='anIdent-with-dashes')

    def testNumber(self):
        self.assertCSSAttrValueEqual('1', value='1')
        self.assertCSSAttrValueEqual('2.78', value='2.78')
        self.assertCSSAttrValueEqual(('1', 'em'), value='1em')
        self.assertCSSAttrValueEqual(('2.78', 'pt'), value='2.78pt')
        self.assertCSSAttrValueEqual(('1', '%'), value='1%')
        self.assertCSSAttrValueEqual(('2.78', '%'), value='2.78%')

    def testRGB(self):
        self.assertCSSAttrValueEqual('#ffee00', value='#ffee00')
        self.assertCSSAttrValueEqual('#fe0', value='#fe0')

    def testURLs(self):
        result = 'http://stuff.com/more'
        self.assertCSSAttrValueEqual(result, value='url(\'%s\')'%result)
        self.assertCSSAttrValueEqual(result, value='url(\"%s\")'%result)
        self.assertCSSAttrValueEqual(result, value='url(%s)'%result)

        self.assertCSSAttrValueEqual(result, value='url( \'%s\')'%result)
        self.assertCSSAttrValueEqual(result, value='url( \"%s\")'%result)
        self.assertCSSAttrValueEqual(result, value='url( %s)'%result)
        self.assertCSSAttrValueEqual(result, value='url(\'%s\' )'%result)
        self.assertCSSAttrValueEqual(result, value='url(\"%s\" )'%result)
        self.assertCSSAttrValueEqual(result, value='url(%s )'%result)
        self.assertCSSAttrValueEqual(result, value='url( \'%s\' )'%result)
        self.assertCSSAttrValueEqual(result, value='url( \"%s\" )'%result)
        self.assertCSSAttrValueEqual(result, value='url( %s )'%result)
    

    def testFunction(self):
        def assertEqualFn(result, (name, params)):
            self.assertEqual(result.name, name)
            self.assertEqual(result.params, params)

        self.assertCSSAttrValueEqual(('testFn', ['aParam']), equalfn=assertEqualFn,
                value='testFn(aParam)')
        self.assertCSSAttrValueEqual(('testFn', ['aParam1', 'aParam2']), assertEqualFn,
                value='testFn(aParam1, aParam2)')
        self.assertCSSAttrValueEqual(('testFn', ['aParam1', 'aParam2']), assertEqualFn,
                value='testFn(aParam1 aParam2)')
        self.assertCSSAttrValueEqual(
                ('testFn', ['aParam', '1', '1.2', ('10', '%'), ('10.5', '%'), "aString", 'another', '#c0ffee', 'http://stuff.com/more']), 
                equalfn=assertEqualFn,
                value='testFn(aParam, 1, 1.2, 10%, 10.5%, "aString", \'another\', #c0ffee, url(http://stuff.com/more))')

    def testIdentList(self):
        result = 'anIdent anIdent-with-dashes _anUnderScore'.split()
        self.assertCSSAttrValueEqual(result, value='anIdent anIdent-with-dashes _anUnderScore')
        self.assertCSSAttrValueEqual(result, value='anIdent, anIdent-with-dashes, _anUnderScore')

        self.assertCSSAttrValueEqual(result, value='anIdent anIdent-with-dashes, _anUnderScore,')
        self.assertCSSAttrValueEqual(result, value='anIdent, anIdent-with-dashes, _anUnderScore,')

    def testMixedList(self):
        result = ['aParam', '1', '1.2', ('10', '%'), ('10.5', '%'), "aString", 'another', '#c0ffee', 'http://stuff.com/more']
        self.assertCSSAttrValueEqual(result, value='aParam, 1, 1.2, 10%, 10.5%, "aString", \'another\', #c0ffee, url(http://stuff.com/more)')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TestCSSInline(unittest.TestCase):
    def setUp(self):
        self.parser = css.CSSParser()

    def assertCSSValueEqual(self, testcss, good, equalfn=None):
        if equalfn is None: equalfn = self.assertEqual
        fn = lambda r, v: equalfn(r['value'], v)
        self.assertCSSEqual(testcss, good, fn)

    def assertCSSEqual(self, testcss, good, equalfn=None):
        if equalfn is None:
            equalfn = self.assertEqual
        result = self.parser.parseInline(testcss)
        equalfn(result, good)
        result = self.parser.parseInline('{'+testcss+'}')
        equalfn(result, good)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Tests
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testOneValue(self):
        result = {'one':'1'}
        self.assertCSSEqual('one: 1', result)
        self.assertCSSEqual('one:1', result)
        self.assertCSSEqual('one 1', {})

    def testMultipleValue(self):
        result = {'one':'1', 'two':'2', 'three':'3'}
        self.assertCSSEqual('one: 1;two: 2;three: 3', result)
        self.assertCSSEqual('one:1;two:2;three:3', result)
        self.assertCSSEqual('one 1;two 2;three 3', {})

    def testListValue(self):
        result = ['1','2','3','4','5']
        self.assertCSSValueEqual('value: 1, 2, 3, 4, 5,', result)
        self.assertCSSValueEqual('value: 1, 2, 3, 4, 5,', result)
        self.assertCSSValueEqual('value: 1 2 3 4 5', result)
        self.assertCSSValueEqual('value: 1 2 3, 4 5,', result)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testIdent(self):
        self.assertCSSValueEqual('value: anIdent', 'anIdent')
        self.assertCSSValueEqual('value: anIdent-with-dashes', 'anIdent-with-dashes')

    def testNumber(self):
        self.assertCSSValueEqual('value: 1', '1')
        self.assertCSSValueEqual('value: 2.78', '2.78')
        self.assertCSSValueEqual('value: 1em', ('1', 'em'))
        self.assertCSSValueEqual('value: 2.78pt', ('2.78', 'pt'))
        self.assertCSSValueEqual('value: 1%', ('1', '%'))
        self.assertCSSValueEqual('value: 2.78%', ('2.78', '%'))

    def testString(self):
        result = 'a test string'
        self.assertCSSValueEqual('value: \'%s\''%result, result)
        self.assertCSSValueEqual('value: \"%s\"'%result, result)

    def testRGB(self):
        self.assertCSSValueEqual('value: #ffee00', '#ffee00')
        self.assertCSSValueEqual('value: #fe0', '#fe0')

    def testURLs(self):
        result = 'http://stuff.com/more'
        self.assertCSSValueEqual('value: url(\'%s\')'%result, result)
        self.assertCSSValueEqual('value: url(\"%s\")'%result, result)
        self.assertCSSValueEqual('value: url(%s)'%result, result)

    def testFunction(self):
        def assertEqualFn(result, (name, params)):
            self.assertEqual(result.name, name)
            self.assertEqual(result.params, params)

        self.assertCSSValueEqual('value: testFn(aParam)', ('testFn', ['aParam']), assertEqualFn)
        self.assertCSSValueEqual('value: testFn(aParam1, aParam2)', ('testFn', ['aParam1', 'aParam2']), assertEqualFn)
        self.assertCSSValueEqual('value: testFn(aParam1 aParam2)', ('testFn', ['aParam1', 'aParam2']), assertEqualFn)
        self.assertCSSValueEqual('value: testFn(aParam, 1, 1.2, 10%, 10.5%, "aString", \'another\', #c0ffee, url(http://stuff.com/more))', 
                ('testFn', ['aParam', '1', '1.2', ('10', '%'), ('10.5', '%'), "aString", 'another', '#c0ffee', 'http://stuff.com/more']), assertEqualFn)

    def testIdentList(self):
        result = 'anIdent anIdent-with-dashes _anUnderScore'.split()
        self.assertCSSValueEqual('value: anIdent anIdent-with-dashes _anUnderScore', result)
        self.assertCSSValueEqual('value: anIdent, anIdent-with-dashes, _anUnderScore', result)

        self.assertCSSValueEqual('value: anIdent anIdent-with-dashes, _anUnderScore,', result)
        self.assertCSSValueEqual('value: anIdent, anIdent-with-dashes, _anUnderScore,', result)

    def testMixedList(self):
        result = ['aParam', '1', '1.2', ('10', '%'), ('10.5', '%'), "aString", 'another', '#c0ffee', 'http://stuff.com/more']
        self.assertCSSValueEqual('value: aParam, 1, 1.2, 10%, 10.5%, "aString", \'another\', #c0ffee, url(http://stuff.com/more)', result)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TestCSSSelectors(unittest.TestCase):
    def setUp(self):
        self.parser = css.CSSParser()
    def tearDown(self):
        del self.parser

    def parseCSS(self, testcss):
        return self.parser.parse(testcss)

    def assertSpecifityEqual(self, testcss, goodValue):
        stylesheet = self.parseCSS(testcss)
        for selector in stylesheet.iterkeys():
            self.assertEqual(selector.specificity(), goodValue)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testSimplest(self):
        stylesheet = self.parseCSS('node{value: 1}')
        self.assertEqual(len(stylesheet), 1)

        (selector, declarations), = stylesheet.items()
        self.assertEqual(selector.name, 'node')
        self.assertEqual(selector.qualifiers, ())
        self.assertEqual(declarations, {'value':'1'})

    def testMultiple(self):
        stylesheet = self.parseCSS('nodeA, nodeB, nodeC {value: 1}')
        for selector, declarations in stylesheet.items():
            self.assertEqual(declarations , {'value':'1'})
            self.assert_(selector.name in ('nodeA', 'nodeB', 'nodeC'))
            self.assertEqual(selector.qualifiers, ())

    def testCommentInString(self):
        stylesheet = self.parseCSS('node{start: "stuff /* here"; stop: "more */ stuff"; /* not-included: True */}')
        self.assertEqual(len(stylesheet), 1)

        (selector, declarations), = stylesheet.items()
        self.assertEqual(selector.name, 'node')
        self.assertEqual(selector.qualifiers, ())
        self.assertEqual(len(declarations), 2)
        self.assertEqual(declarations, {'start':'stuff /* here', 'stop':'more */ stuff'})

    def testMultipleWithNewlines(self):
        stylesheet = self.parseCSS('nodeA,\nnodeB,\nnodeC\n{value: 1}')
        for selector, declarations in stylesheet.items():
            self.assertEqual(declarations , {'value':'1'})
            self.assert_(selector.name in ('nodeA', 'nodeB', 'nodeC'))
            self.assertEqual(selector.qualifiers, ())

    def testMultipleBlocks(self):
        stylesheet = self.parseCSS('nodeA{value: 1}nodeB.myClass{stuff: 2}nodeC#myId{grok:"yes"}')
        for selector, declarations in stylesheet.items():
            if selector.name == 'nodeA':
                self.assertEqual(declarations, {'value':'1'})
                self.assertEqual(selector.qualifiers, ())
            elif selector.name == 'nodeB':
                self.assertEqual(declarations, {'stuff':'2'})
                self.assertEqual(selector.qualifiers[0].classId, 'myClass')
            elif selector.name == 'nodeC':
                self.assertEqual(declarations, {'grok':'yes'})
                self.assertEqual(selector.qualifiers[0].hashId, 'myId')
            else:
                self.fail('Expected a selector name of "nodeA", "nodeB", or "nodeC", but found' + selector.name)

    def testId(self):
        stylesheet = self.parseCSS('node#myId{value: 1}')
        for selector, declarations in stylesheet.items():
            self.assertEqual(declarations, {'value':'1'})
            self.assertEqual(selector.name, 'node')
            self.assertEqual(selector.qualifiers[0].hashId, 'myId')

    def testClass(self):
        stylesheet = self.parseCSS('node.myClass{value: 1}')
        for selector, declarations in stylesheet.items():
            self.assertEqual(declarations, {'value':'1'})
            self.assertEqual(selector.name, 'node')
            self.assertEqual(selector.qualifiers[0].classId, 'myClass')

    def testClassId(self):
        stylesheet = self.parseCSS('node.myClass#myId{value: 1}')
        for selector, declarations in stylesheet.items():
            self.assertEqual(declarations, {'value':'1'})
            self.assertEqual(selector.name, 'node')
            self.assertEqual(selector.qualifiers[0].classId, 'myClass')
            self.assertEqual(selector.qualifiers[1].hashId, 'myId')

    def testIdClass(self):
        stylesheet = self.parseCSS('node#myId.myClass{value: 1}')
        for selector, declarations in stylesheet.items():
            self.assertEqual(declarations, {'value':'1'})
            self.assertEqual(selector.name, 'node')
            self.assertEqual(selector.qualifiers[0].hashId, 'myId')
            self.assertEqual(selector.qualifiers[1].classId, 'myClass')

    def testAttributeExists(self):
        stylesheet = self.parseCSS('node[myAttr]{value: 1}')
        for selector, declarations in stylesheet.items():
            self.assertEqual(declarations, {'value':'1'})
            self.assertEqual(selector.name, 'node')
            self.assertEqual(selector.qualifiers[0].name, 'myAttr')
            self.assertEqual(selector.qualifiers[0].op, None)
            self.assertEqual(selector.qualifiers[0].value, NotImplemented)

    def testAttributeEqual(self):
        stylesheet = self.parseCSS('node[myAttr=something]{value: 1}')
        for selector, declarations in stylesheet.items():
            self.assertEqual(declarations, {'value':'1'})
            self.assertEqual(selector.name, 'node')
            self.assertEqual(selector.qualifiers[0].name, 'myAttr')
            self.assertEqual(selector.qualifiers[0].op, '=')
            self.assertEqual(selector.qualifiers[0].value, 'something')

    def testAttributeContains(self):
        stylesheet = self.parseCSS('node[myAttr~=something]{value: 1}')
        for selector, declarations in stylesheet.items():
            self.assertEqual(declarations, {'value':'1'})
            self.assertEqual(selector.name, 'node')
            self.assertEqual(selector.qualifiers[0].name, 'myAttr')
            self.assertEqual(selector.qualifiers[0].op, '~=')
            self.assertEqual(selector.qualifiers[0].value, 'something')

    def testAttributeContains2(self):
        stylesheet = self.parseCSS('node[myAttr|=something]{value: 1}')
        for selector, declarations in stylesheet.items():
            self.assertEqual(declarations, {'value':'1'})
            self.assertEqual(selector.name, 'node')
            self.assertEqual(selector.qualifiers[0].name, 'myAttr')
            self.assertEqual(selector.qualifiers[0].op, '|=')
            self.assertEqual(selector.qualifiers[0].value, 'something')

    def testPseudo(self):
        stylesheet = self.parseCSS('node:myPseudo{value: 1}')
        for selector, declarations in stylesheet.items():
            self.assertEqual(declarations, {'value':'1'})
            self.assertEqual(selector.name, 'node')
            self.assertEqual(selector.qualifiers[0].name, 'myPseudo')
            self.assertEqual(selector.qualifiers[0].params, ())

    def testPseudoFn(self):
        stylesheet = self.parseCSS('node:myPseudo(paramA){value: 1}')
        for selector, declarations in stylesheet.items():
            self.assertEqual(declarations, {'value':'1'})
            self.assertEqual(selector.name, 'node')
            self.assertEqual(selector.qualifiers[0].name, 'myPseudo')
            self.assertEqual(selector.qualifiers[0].params, ('paramA',))

        stylesheet = self.parseCSS('node:myPseudo(paramA, paramB){value: 1}')
        for selector, declarations in stylesheet.items():
            self.assertEqual(declarations, {'value':'1'})
            self.assertEqual(selector.name, 'node')
            self.assertEqual(selector.qualifiers[0].name, 'myPseudo')
            self.assertEqual(selector.qualifiers[0].params, ('paramA', 'paramB'))

        stylesheet = self.parseCSS('node:myPseudo(paramA paramB){value: 1}')
        for selector, declarations in stylesheet.items():
            self.assertEqual(declarations, {'value':'1'})
            self.assertEqual(selector.name, 'node')
            self.assertEqual(selector.qualifiers[0].name, 'myPseudo')
            self.assertEqual(selector.qualifiers[0].params, ('paramA', 'paramB'))

    def testCombinerPlain(self):
        stylesheet = self.parseCSS('nodeA nodeB {value: 1}')
        for selector, declarations in stylesheet.items():
            self.assertEqual(declarations, {'value':'1'})
            self.assertEqual(selector.name, 'nodeB')
            self.assertEqual(selector.qualifiers[0].op, ' ')
            self.assertEqual(selector.qualifiers[0].selector.name, 'nodeA')
            self.assertEqual(selector.qualifiers[0].selector.qualifiers, ())

    def testCombinerAdd(self):
        stylesheet = self.parseCSS('nodeA + nodeB {value: 1}')
        for selector, declarations in stylesheet.items():
            self.assertEqual(declarations, {'value':'1'})
            self.assertEqual(selector.name, 'nodeB')
            self.assertEqual(selector.qualifiers[0].op, '+')
            self.assertEqual(selector.qualifiers[0].selector.name, 'nodeA')
            self.assertEqual(selector.qualifiers[0].selector.qualifiers, ())

    def testCombinerGreater(self):
        stylesheet = self.parseCSS('nodeA > nodeB {value: 1}')
        for selector, declarations in stylesheet.items():
            self.assertEqual(declarations, {'value':'1'})
            self.assertEqual(selector.name, 'nodeB')
            self.assertEqual(selector.qualifiers[0].op, '>')
            self.assertEqual(selector.qualifiers[0].selector.name, 'nodeA')
            self.assertEqual(selector.qualifiers[0].selector.qualifiers, ())

    def testSpecifity(self):
        self.assertSpecifityEqual('*             {}', (0,0,0,0))
        self.assertSpecifityEqual('li            {}', (0,0,0,1))
        self.assertSpecifityEqual('li:first-line {}', (0,0,0,2))
        self.assertSpecifityEqual('ul li         {}', (0,0,0,2))
        self.assertSpecifityEqual('ul ol+li      {}', (0,0,0,3))
        self.assertSpecifityEqual('h1 + *[rel=up]{}', (0,0,1,1))
        self.assertSpecifityEqual('ul ol li.red  {}', (0,0,1,3))
        self.assertSpecifityEqual('li.red.level  {}', (0,0,2,1))
        self.assertSpecifityEqual('#x34y         {}', (0,1,0,0))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testAnyId(self):
        stylesheet = self.parseCSS('*#myId{value: 1}')
        for selector, declarations in stylesheet.items():
            self.assertEqual(declarations, {'value':'1'})
            self.assertEqual(selector.name, '*')
            self.assertEqual(selector.qualifiers[0].hashId, 'myId')

        stylesheet = self.parseCSS('#myId{value: 1}')
        for selector, declarations in stylesheet.items():
            self.assertEqual(declarations, {'value':'1'})
            self.assertEqual(selector.name, '*')
            self.assertEqual(selector.qualifiers[0].hashId, 'myId')

    def testAnyClass(self):
        stylesheet = self.parseCSS('*.myClass{value: 1}')
        for selector, declarations in stylesheet.items():
            self.assertEqual(declarations, {'value':'1'})
            self.assertEqual(selector.name, '*')
            self.assertEqual(selector.qualifiers[0].classId, 'myClass')

        stylesheet = self.parseCSS('.myClass{value: 1}')
        for selector, declarations in stylesheet.items():
            self.assertEqual(declarations, {'value':'1'})
            self.assertEqual(selector.name, '*')
            self.assertEqual(selector.qualifiers[0].classId, 'myClass')

    def testAnyClassId(self):
        stylesheet = self.parseCSS('*.myClass#myId{value: 1}')
        for selector, declarations in stylesheet.items():
            self.assertEqual(declarations, {'value':'1'})
            self.assertEqual(selector.name, '*')
            self.assertEqual(selector.qualifiers[0].classId, 'myClass')
            self.assertEqual(selector.qualifiers[1].hashId, 'myId')

        stylesheet = self.parseCSS('.myClass#myId{value: 1}')
        for selector, declarations in stylesheet.items():
            self.assertEqual(declarations, {'value':'1'})
            self.assertEqual(selector.name, '*')
            self.assertEqual(selector.qualifiers[0].classId, 'myClass')
            self.assertEqual(selector.qualifiers[1].hashId, 'myId')

    def testAnyIdClass(self):
        stylesheet = self.parseCSS('*#myId.myClass{value: 1}')
        for selector, declarations in stylesheet.items():
            self.assertEqual(declarations, {'value':'1'})
            self.assertEqual(selector.name, '*')
            self.assertEqual(selector.qualifiers[0].hashId, 'myId')
            self.assertEqual(selector.qualifiers[1].classId, 'myClass')

        stylesheet = self.parseCSS('#myId.myClass{value: 1}')
        for selector, declarations in stylesheet.items():
            self.assertEqual(declarations, {'value':'1'})
            self.assertEqual(selector.name, '*')
            self.assertEqual(selector.qualifiers[0].hashId, 'myId')
            self.assertEqual(selector.qualifiers[1].classId, 'myClass')

    def testAnyAttributeExists(self):
        stylesheet = self.parseCSS('*[myAttr]{value: 1}')
        for selector, declarations in stylesheet.items():
            self.assertEqual(declarations, {'value':'1'})
            self.assertEqual(selector.name, '*')
            self.assertEqual(selector.qualifiers[0].name, 'myAttr')
            self.assertEqual(selector.qualifiers[0].op, None)
            self.assertEqual(selector.qualifiers[0].value, NotImplemented)

        stylesheet = self.parseCSS('[myAttr]{value: 1}')
        for selector, declarations in stylesheet.items():
            self.assertEqual(declarations, {'value':'1'})
            self.assertEqual(selector.name, '*')
            self.assertEqual(selector.qualifiers[0].name, 'myAttr')
            self.assertEqual(selector.qualifiers[0].op, None)
            self.assertEqual(selector.qualifiers[0].value, NotImplemented)

    def testAnyAttributeEqual(self):
        stylesheet = self.parseCSS('*[myAttr=something]{value: 1}')
        for selector, declarations in stylesheet.items():
            self.assertEqual(declarations, {'value':'1'})
            self.assertEqual(selector.name, '*')
            self.assertEqual(selector.qualifiers[0].name, 'myAttr')
            self.assertEqual(selector.qualifiers[0].op, '=')
            self.assertEqual(selector.qualifiers[0].value, 'something')

        stylesheet = self.parseCSS('[myAttr=something]{value: 1}')
        for selector, declarations in stylesheet.items():
            self.assertEqual(declarations, {'value':'1'})
            self.assertEqual(selector.name, '*')
            self.assertEqual(selector.qualifiers[0].name, 'myAttr')
            self.assertEqual(selector.qualifiers[0].op, '=')
            self.assertEqual(selector.qualifiers[0].value, 'something')

    def testAnyAttributeContains(self):
        stylesheet = self.parseCSS('*[myAttr~=something]{value: 1}')
        for selector, declarations in stylesheet.items():
            self.assertEqual(declarations, {'value':'1'})
            self.assertEqual(selector.name, '*')
            self.assertEqual(selector.qualifiers[0].name, 'myAttr')
            self.assertEqual(selector.qualifiers[0].op, '~=')
            self.assertEqual(selector.qualifiers[0].value, 'something')

        stylesheet = self.parseCSS('[myAttr~=something]{value: 1}')
        for selector, declarations in stylesheet.items():
            self.assertEqual(declarations, {'value':'1'})
            self.assertEqual(selector.name, '*')
            self.assertEqual(selector.qualifiers[0].name, 'myAttr')
            self.assertEqual(selector.qualifiers[0].op, '~=')
            self.assertEqual(selector.qualifiers[0].value, 'something')

    def testAnyAttributeContains2(self):
        stylesheet = self.parseCSS('*[myAttr|=something]{value: 1}')
        for selector, declarations in stylesheet.items():
            self.assertEqual(declarations, {'value':'1'})
            self.assertEqual(selector.name, '*')
            self.assertEqual(selector.qualifiers[0].name, 'myAttr')
            self.assertEqual(selector.qualifiers[0].op, '|=')
            self.assertEqual(selector.qualifiers[0].value, 'something')

        stylesheet = self.parseCSS('[myAttr|=something]{value: 1}')
        for selector, declarations in stylesheet.items():
            self.assertEqual(declarations, {'value':'1'})
            self.assertEqual(selector.name, '*')
            self.assertEqual(selector.qualifiers[0].name, 'myAttr')
            self.assertEqual(selector.qualifiers[0].op, '|=')
            self.assertEqual(selector.qualifiers[0].value, 'something')

    def testAnyPseudo(self):
        stylesheet = self.parseCSS('*:myPseudo{value: 1}')
        for selector, declarations in stylesheet.items():
            self.assertEqual(declarations, {'value':'1'})
            self.assertEqual(selector.name, '*')
            self.assertEqual(selector.qualifiers[0].name, 'myPseudo')
            self.assertEqual(selector.qualifiers[0].params, ())

        stylesheet = self.parseCSS(':myPseudo{value: 1}')
        for selector, declarations in stylesheet.items():
            self.assertEqual(declarations, {'value':'1'})
            self.assertEqual(selector.name, '*')
            self.assertEqual(selector.qualifiers[0].name, 'myPseudo')
            self.assertEqual(selector.qualifiers[0].params, ())

    def testAnyPseudoFn(self):
        stylesheet = self.parseCSS('*:myPseudo(paramA){value: 1}')
        for selector, declarations in stylesheet.items():
            self.assertEqual(declarations, {'value':'1'})
            self.assertEqual(selector.name, '*')
            self.assertEqual(selector.qualifiers[0].name, 'myPseudo')
            self.assertEqual(selector.qualifiers[0].params, ('paramA',))

        stylesheet = self.parseCSS(':myPseudo(paramA){value: 1}')
        for selector, declarations in stylesheet.items():
            self.assertEqual(declarations, {'value':'1'})
            self.assertEqual(selector.name, '*')
            self.assertEqual(selector.qualifiers[0].name, 'myPseudo')
            self.assertEqual(selector.qualifiers[0].params, ('paramA',))

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        stylesheet = self.parseCSS('*:myPseudo(paramA, paramB){value: 1}')
        for selector, declarations in stylesheet.items():
            self.assertEqual(declarations, {'value':'1'})
            self.assertEqual(selector.name, '*')
            self.assertEqual(selector.qualifiers[0].name, 'myPseudo')
            self.assertEqual(selector.qualifiers[0].params, ('paramA', 'paramB'))

        stylesheet = self.parseCSS(':myPseudo(paramA, paramB){value: 1}')
        for selector, declarations in stylesheet.items():
            self.assertEqual(declarations, {'value':'1'})
            self.assertEqual(selector.name, '*')
            self.assertEqual(selector.qualifiers[0].name, 'myPseudo')
            self.assertEqual(selector.qualifiers[0].params, ('paramA', 'paramB'))

    def testAnyCombinerPlain(self):
        stylesheet = self.parseCSS('* nodeB {value: 1}')
        for selector, declarations in stylesheet.items():
            self.assertEqual(declarations, {'value':'1'})
            self.assertEqual(selector.name, 'nodeB')
            self.assertEqual(selector.qualifiers[0].op, ' ')
            self.assertEqual(selector.qualifiers[0].selector.name, '*')
            self.assertEqual(selector.qualifiers[0].selector.qualifiers, ())

    def testAnyCombinerAdd(self):
        stylesheet = self.parseCSS('* + nodeB {value: 1}')
        for selector, declarations in stylesheet.items():
            self.assertEqual(declarations, {'value':'1'})
            self.assertEqual(selector.name, 'nodeB')
            self.assertEqual(selector.qualifiers[0].op, '+')
            self.assertEqual(selector.qualifiers[0].selector.name, '*')
            self.assertEqual(selector.qualifiers[0].selector.qualifiers, ())

    def testAnyCombinerGreater(self):
        stylesheet = self.parseCSS('* > nodeB {value: 1}')
        for selector, declarations in stylesheet.items():
            self.assertEqual(declarations, {'value':'1'})
            self.assertEqual(selector.name, 'nodeB')
            self.assertEqual(selector.qualifiers[0].op, '>')
            self.assertEqual(selector.qualifiers[0].selector.name, '*')
            self.assertEqual(selector.qualifiers[0].selector.qualifiers, ())


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TestCSSAtRules(unittest.TestCase):
    def setUp(self):
        self.builder = css.CSSBuilder()
        self.builder.atImport = self._atImport
        self.builder.atMedia = self._atMedia
        self.builder.atPage = self._atPage
        self.builder.atPageMargin = self._atPageMargin
        self.builder.atFontFace = self._atFontFace
        self.parser = css.CSSParser(self.builder)

        self.cssImportString = None
        self.goodImportValue = None
        self.goodMediumValue = None

    def tearDown(self):
        del self.parser

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _atMedia(self, mediums, ruleset):
        self.assertEqual(mediums, self.goodMediumValue)
        return ruleset

    def _atImport(self, import_, mediums, cssParser):
        self.assert_(self.parser is cssParser)
        self.assertEqual(import_, self.goodImportValue)
        self.assertEqual(mediums, self.goodMediumValue)
        if self.cssImportString is not None:
            return cssParser.parse(self.cssImportString)
        else: return None

    def _atPage(self, page, pseudoPage, properties, margins):
        self._atPageArgs = page, pseudoPage, dict([(n,v) for n,v,i in properties]), margins
        return [dict([(n,v) for n,v,i in properties])]

    def _atPageMargin(self, page, pseudoPage, marginName, properties):
        return (marginName, dict([(n,v) for n,v,i in properties]))

    def _atFontFace(self, declarations):
        self._atFontFaceArgs = dict([(n,v) for n,v,i in declarations])
        return [self._atFontFaceArgs]

    def _atIdent(self, atIdent, cssParser, src):
        self._atIdentCalled = atIdent
        return src, None

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _checkResultStylesheet(self, stylesheet):
        for selector, declarations in stylesheet.items():
            self.assertEqual(declarations, {'value':'1'})
            self.assertEqual(selector.name, 'node')
            self.assertEqual(selector.qualifiers, ())

    def parseCSS(self, testcss):
        return self.parser.parse(testcss)

    def testAtImport(self):
        self.cssImportString = 'node{value: 1}'
        self.goodImportValue = 'stuff'
        self.goodMediumValue = []
        stylesheet = self.parseCSS('@import "%s";'%self.goodImportValue)
        self._checkResultStylesheet(stylesheet)
        stylesheet = self.parseCSS('@import \'%s\';'%self.goodImportValue)
        self._checkResultStylesheet(stylesheet)

    def testAtImportWithMediums(self):
        self.cssImportString = 'node{value: 1}'
        self.goodImportValue = 'otherStuff'
        self.goodMediumValue = ['paper', 'towel']
        stylesheet = self.parseCSS('@import url("%s") paper, towel;'%self.goodImportValue)
        self._checkResultStylesheet(stylesheet)
        stylesheet = self.parseCSS('@import url(%s) paper, towel;'%self.goodImportValue)
        self._checkResultStylesheet(stylesheet)

    def testAtNamespace(self):
        testcss = """
        @namespace "default:namespace";
        @namespace foo "foo:namespace";

        |node{color: black}
        |*{color: black}

        *|node{color: black}
        *|*{color: black}

        foo|node{color: black}
        foo|*{color: black}
        """
        stylesheet = self.parseCSS(testcss)

        for selector, declarations in stylesheet.items():
            self.assertEqual(declarations,{'color': 'black'})

            if selector.nsPrefix == '':
                self.assert_(selector.name in ('*', 'node'))
                self.assertEqual(selector.namespace, None)
            elif selector.nsPrefix == '*':
                self.assert_(selector.name in ('*', 'node'))
                self.assertEqual(selector.namespace, "*")
            elif selector.nsPrefix == 'foo':
                self.assert_(selector.name in ('*', 'node'))
                self.assertEqual(selector.namespace, "foo:namespace")
            else:
                self.fail('Invalid state for selector %r'%selector)

    def testAtMedia(self):
        self.goodMediumValue = ['paper']
        stylesheet = self.parseCSS('@media paper {node{value: 1}}')
        self._checkResultStylesheet(stylesheet)

        self.goodMediumValue = ['paper', 'towel']
        stylesheet = self.parseCSS('@media paper, towel {node{value: 1}}')
        self._checkResultStylesheet(stylesheet)

    def testAtPage(self):
        self._atPageArgs = ()
        stylesheet = self.parseCSS('@page {value: 1}')
        self.assertEqual(self._atPageArgs, ('', '', {'value': '1'}, []))

        self._atPageArgs = ()
        stylesheet = self.parseCSS('@page myPage {value: 1}')
        self.assertEqual(self._atPageArgs, ('myPage', '', {'value': '1'}, []))

        self._atPageArgs = ()
        stylesheet = self.parseCSS('@page myPage:myPseudoPage {value: 1}')
        self.assertEqual(self._atPageArgs, ('myPage','myPseudoPage', {'value': '1'}, []))

    def testAtPageMargins(self):
        self._atPageArgs = ()
        stylesheet = self.parseCSS('@page {@bottom-center {value: 1} value: 8}')
        self.assertEqual(self._atPageArgs, ('', '', {'value': '8'}, [('bottom-center', {'value': '1'})]))

        self._atPageArgs = ()
        stylesheet = self.parseCSS('@page myPage {@top {value: 1} value: 3}')
        self.assertEqual(self._atPageArgs, ('myPage', '', {'value': '3'}, [('top', {'value': '1'})]))

        self._atPageArgs = ()
        stylesheet = self.parseCSS('@page myPage:myPseudoPage {@left {value: 2} value: 3;}')
        self.assertEqual(self._atPageArgs, ('myPage', 'myPseudoPage', {'value': '3'}, [('left', {'value': '2'})]))

    def testAtFontFace(self):
        self._atFontFaceArgs = None
        stylesheet = self.parseCSS('@font-face {value: 1}')
        self.assertEqual(self._atFontFaceArgs, {'value': '1'})

    def testAtIdent(self):
        def myAtFn(cssParser, atDirective, src):
            self._atIdentCalled = atDirective
            return src, []
        self.parser.atKeywordHandlers['myAtFn'] = myAtFn

        self._atIdentCalled = None
        stylesheet = self.parseCSS('@myAtFn')
        self.assertEqual(self._atIdentCalled, 'myAtFn')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Unittest Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    unittest.main()

