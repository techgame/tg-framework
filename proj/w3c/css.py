#!/usr/bin/env python
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##~ Copyright (C) 2002-2004  TechGame Networks, LLC.
##~ 
##~ This library is free software; you can redistribute it and/or
##~ modify it under the terms of the BSD style License as found in the 
##~ LICENSE file included with this distribution.
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""CSS-2.1 engine

Primary classes:
    * CSSElementInterfaceAbstract
        Provide a concrete implementation for the XML element model used.

    * CSSCascadeStrategy
        Implements the CSS-2.1 engine's attribute lookup rules.

    * CSSParser
        Parses CSS source forms into usable results using CSSBuilder and
        CSSMutableSelector.  You may want to override parseExternal()

    * CSSBuilder (and CSSMutableSelector)
        A concrete implementation for cssParser.CSSBuilderAbstract (and
        cssParser.CSSSelectorAbstract) to provide usable results to
        CSSParser requests.

Dependencies: 
    python 2.3 (or greater)
        sets
    cssParser
        re

Credits:
    * 2005.07.12 Andre Soereng
        Asked for increased stylesheet merging support to handle multiple
        stylesheet links.  He also noticed that the CSS Cascading rules were
        not correct.  (In fact, they were exactly backwards ;)  A new tests was
        added to verify the cascading order.

    * 2005.03.23 Gary Poster
        Host of bugfixes and testing of the engine.  He also added support for 
        page margins from http://www.w3.org/TR/css3-page/

"""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os
import itertools

try: 
    set
except NameError:
    from sets import Set as set

import cssParser

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Constants / Variables / Etc. 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

CSSParseError = cssParser.CSSParseError

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CSSElementInterfaceAbstract(object):
    def asCSSElement(self):
        return self
    def getAttr(self, name, default=NotImplemented): 
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def getIdAttr(self): 
        return self.getAttr('id', '')
    def getClassAttr(self): 
        return self.getAttr('class', '')
    def getClasses(self): 
        return self.getClassAttr().replace(',', ' ').split()

    def getInlineStyle(self): 
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def setInlineStyle(self, style):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def getInlineStyleEx(self, fnParseInline=None):
        style = self.getInlineStyle()
        if fnParseInline and style:
            style = fnParseInline(self.getStyleAttr() or '')
            self.setInlineStyle(style)
        return style

    def getInlineStyleEx(self, fnParseInline=None): 
        return self.getInlineStyle()

    def matchesNode(self): 
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

    def inPseudoState(self, name, params=()): 
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

    def iterXMLParents(self): 
        """Results must be compatible with CSSElementInterfaceAbstract"""
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

    def getPreviousSibling(self): 
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

class CSSElementInterfaceBase(CSSElementInterfaceAbstract):
    def getStyleAttr(self):
        return self.getAttr('style', '')

    _inlineStyle = None
    def getInlineStyle(self):
        return self._inlineStyle
    def setInlineStyle(self, style):
        self._inlineStyle = style
    def delInlineStyle(self):
        del self._inlineStyle

    def getInlineStyleEx(self, fnParseInline=None):
        style = self.getInlineStyle()
        if fnParseInline and style:
            style = fnParseInline(self.getStyleAttr() or '')
            self.setInlineStyle(style)
        return style

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CSSCascadeStrategy(object):
    author = None
    user = None
    userAgent = None
    _parser = None

    def __init__(self, author=None, user=None, userAgent=None):
        if author is not None:
            self.author = author
        if user is not None:
            self.user = user
        if userAgent is not None:
            self.userAgent = userAgent

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getParser(self):
        return self._parser
    def setParser(self, cssParser):
        self._parser = cssParser

    def getInlineParser(self):
        parser = self.getParser()
        if parser:
            return parser.parseInline

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def copy(self):
        return self.__class__(
                self.author and self.author.copy(), 
                self.user and self.user.copy(), 
                self.userAgent and self.userAgent.copy())

    def merge(self, author=None, user=None, userAgent=None):
        if self.author:
            self.author.merge(author)
        elif author: self.author = author

        if self.user:
            self.user.merge(user)
        elif user: self.user = user

        if self.userAgent:
            self.userAgent.merge(userAgent)
        elif userAgent: self.userAgent = userAgent

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def iterCSSRulesets(self, inline=None):
        """Rulesets, in order of importance specified by the CSS spec.

        .. [1] http://www.w3.org/TR/CSS21/cascade.html#cascading-order
        """
        if self.user is not None:
            yield self.user.important

        if inline:
            yield inline.important
            yield inline.normal

        if self.author is not None:
            yield self.author.important
            yield self.author.normal

        if self.user is not None:
            yield self.user.normal

        if self.userAgent is not None:
            yield self.userAgent.important
            yield self.userAgent.normal

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def findStyleFor(self, element, attrName, default=NotImplemented):
        """Attempts to find the style setting for attrName in the CSSRulesets.

        Note: This method does not attempt to resolve rules that return
        "inherited", "default", or values that have units (including "%").
        This is left up to the client app to re-query the CSS in order to
        implement these semantics.
        """
        attrName = self._normalizeAttrNames(attrName)
        element = self._normalizeCSSElement(element)

        rule = self.findCSSRulesFor(element, attrName)
        return self._extractStyleForRule(rule, attrName, default)

    def findStylesForEach(self, element, attrNames, default=NotImplemented):
        """Attempts to find the style setting for attrName in the CSSRulesets.

        Note: This method does not attempt to resolve rules that return
        "inherited", "default", or values that have units (including "%").
        This is left up to the client app to re-query the CSS in order to
        implement these semantics.
        """
        attrNames = self._normalizeAttrNames(attrNames)
        element = self._normalizeCSSElement(element)

        rules = self.findCSSRulesForEach(element, attrNames)
        return [(attrName, self._extractStyleForRule(rule, attrName, default)) 
                for attrName, rule in rules.iteritems()]
            
    def findAllCSSRulesFor(self, element, bSorted=False):
        result = self._findAllCSSRulesFor(element)
        if bSorted:
            result = sorted(result, reverse=True)
        return result
        
    def _findAllCSSRulesFor(self, element):
        element = self._normalizeCSSElement(element)
        inline = element.getInlineStyleEx(self.getInlineParser())
        for ruleset in self.iterCSSRulesets(inline):
            for rule in ruleset.findAllCSSRulesFor(element):
                yield rule

    def findCSSRulesFor(self, element, attrName):
        element = self._normalizeCSSElement(element)
        attrName = self._normalizeAttrNames(attrName)

        rules = []
        inline = element.getInlineStyleEx(self.getInlineParser())
        for ruleset in self.iterCSSRulesets(inline):
            rules = ruleset.findCSSRuleFor(element, attrName)
            if rules: 
                break
        return rules

    def findCSSRulesForEach(self, element, attrNames):
        element = self._normalizeCSSElement(element)
        attrNames = self._normalizeAttrNames(attrNames)

        allRules = dict([(name, []) for name in attrNames])
        attrNameSet = set(attrNames)

        inline = element.getInlineStyleEx(self.getInlineParser())
        for ruleset in self.iterCSSRulesets(inline):
            for attrName in attrNameSet:
                rules = ruleset.findCSSRuleFor(element, attrName)
                if rules:
                    allRules[attrName] = rules
                    attrNameSet.remove(attrName)

            if not attrNameSet:
                break

        return allRules

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _normalizeCSSElement(self, element):
        return element.asCSSElement()

    def _normalizeAttrNames(self, attrNames):
        return attrNames

    def _extractStyleForRule(self, rule, attrName, default=NotImplemented):
        if rule:
            # rule is packed in a list to differentiate from "no rule" vs "rule
            # whose value evalutates as False"
            style = rule[-1][1]
            return style[attrName]
        elif default is not NotImplemented:
            return default
        else:
            raise LookupError("Could not find style for '%s' in %r" % (attrName, rule))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ CSS Selectors
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CSSSelectorBase(object):
    qualifiers = ()
    inline = False
    _hash = None
    _specificity = None

    def __init__(self, completeName='*', qualifiers=qualifiers):
        if not isinstance(completeName, tuple):
            completeName = (None, '*', completeName)
        self.completeName = completeName
        self.qualifiers = qualifiers

    def _updateHash(self):
        self._hash = hash((self.fullName, self.specificity(), self.qualifiers))
    def __hash__(self):
        if self._hash is None:
            return object.__hash__(self)
        else: 
            return self._hash

    def getNSPrefix(self):
        return self.completeName[0]
    nsPrefix = property(getNSPrefix)

    def getName(self):
        return self.completeName[2]
    name = property(getName)

    def getNamespace(self):
        return self.completeName[1]
    namespace = property(getNamespace)

    def getFullName(self):
        return self.completeName[1:3]
    fullName = property(getFullName)

    def __repr__(self):
        strArgs = (self.__class__.__name__,)+self.specificity()+(self.asString(),)
        return '<%s %d:%d:%d:%d %s >' % strArgs

    def __str__(self):
        return self.asString()

    def __cmp__(self, other):
        result = cmp(self.specificity(), other.specificity())
        if result != 0: 
            return result
        result = cmp(self.fullName, other.fullName)
        if result != 0: 
            return result
        result = cmp(self.qualifiers, other.qualifiers)
        return result

    def specificity(self):
        if self._specificity is None:
            self._specificity = self._calcSpecificity()
        return self._specificity

    def _calcSpecificity(self):
        """from http://www.w3.org/TR/CSS21/cascade.html#specificity"""
        hashCount = 0
        qualifierCount = 0
        elementCount = int(self.name != '*')
        for q in self.qualifiers:
            if q.isHash(): hashCount += 1
            elif q.isClass(): qualifierCount += 1
            elif q.isAttr(): qualifierCount += 1
            elif q.isPseudo(): elementCount += 1
            elif q.isCombiner():
                i,h,q,e = q.selector.specificity()
                hashCount += h
                qualifierCount += q
                elementCount += e
        return self.inline, hashCount, qualifierCount, elementCount

    def matches(self, element=None):
        if element is None: 
            return False

        if not element.matchesNode(self.fullName):
            return False

        for qualifier in self.qualifiers:
            if not qualifier.matches(element):
                return False
        else: 
            return True

    def asString(self):
        result = []
        if self.nsPrefix is not None:
            result.append('%s|%s' % (self.nsPrefix, self.name))
        else: result.append(self.name)

        for q in self.qualifiers:
            if q.isCombiner():
                result.insert(0, q.asString())
            else:
                result.append(q.asString())
        return ''.join(result)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CSSInlineSelector(CSSSelectorBase):
    qualifiers = ()
    inline = True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CSSMutableSelector(CSSSelectorBase, cssParser.CSSSelectorAbstract):
    qualifiers = [] # note this is lazyily initialized in _addQualifier

    def asImmutable(self):
        return CSSImmutableSelector(self.completeName, [q.asImmutable() for q in self.qualifiers])

    def combineSelectors(klass, selectorA, op, selectorB):
        selectorB.addCombination(op, selectorA)
        return selectorB
    combineSelectors = classmethod(combineSelectors)

    def addCombination(self, op, other):
        self._addQualifier(CSSSelectorCombinationQualifier(op, other))
    def addHashId(self, hashId):
        self._addQualifier(CSSSelectorHashQualifier(hashId))
    def addClass(self, class_):
        self._addQualifier(CSSSelectorClassQualifier(class_))
    def addAttribute(self, attrName):
        self._addQualifier(CSSSelectorAttributeQualifier(attrName))
    def addAttributeOperation(self, attrName, op, attrValue):
        self._addQualifier(CSSSelectorAttributeQualifier(attrName, op, attrValue))
    def addPseudo(self, name):
        self._addQualifier(CSSSelectorPseudoQualifier(name))
    def addPseudoFunction(self, name, params):
        self._addQualifier(CSSSelectorPseudoQualifier(name, params))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _addQualifier(self, qualifier):
        if self.qualifiers:
            self.qualifiers.append(qualifier)
        else:
            self.qualifiers = [qualifier]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CSSImmutableSelector(CSSSelectorBase):
    qualifiers = ()

    def __init__(self, completeName='*', qualifiers=qualifiers):
        CSSSelectorBase.__init__(self, completeName, tuple(qualifiers))
        self._updateHash()

    def fromSelector(klass, selector):
        return klass(selector.completeName, selector.qualifiers)
    fromSelector = classmethod(fromSelector)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ CSS Selector Qualifiers -- see CSSImmutableSelector
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CSSSelectorQualifierBase(object): 
    def isHash(self): 
        return False
    def isClass(self): 
        return False
    def isAttr(self): 
        return False
    def isPseudo(self): 
        return False
    def isCombiner(self): 
        return False
    def asImmutable(self): 
        return self
    def __str__(self): 
        return self.asString()

class CSSSelectorHashQualifier(CSSSelectorQualifierBase): 
    def __init__(self, hashId):
        self.hashId = hashId
    def isHash(self): 
        return True
    def __hash__(self): 
        return hash((self.hashId,))
    def asString(self): 
        return '#'+self.hashId
    def matches(self, element): 
        return element.getIdAttr() == self.hashId

class CSSSelectorClassQualifier(CSSSelectorQualifierBase):
    def __init__(self, classId):
        self.classId = classId
    def isClass(self): 
        return True
    def __hash__(self): 
        return hash((self.classId,))
    def asString(self): 
        return '.'+self.classId
    def matches(self, element): 
        return self.classId in element.getClasses()

class CSSSelectorAttributeQualifier(CSSSelectorQualifierBase):
    name, op, value = None, None, NotImplemented

    def __init__(self, attrName, op=None, attrValue=NotImplemented):
        self.name = attrName
        if op is not self.op:
            self.op = op 
        if attrValue is not self.value:
            self.value = attrValue
    def isAttr(self): 
        return True
    def __hash__(self): 
        return hash((self.name, self.op, self.value))
    def asString(self): 
        if self.value is NotImplemented:
            return '[%s]' % (self.name,)
        else: return '[%s%s%s]' % (self.name, self.op, self.value)
    def matches(self, element): 
        op = self.op
        if op is None:
            return element.getAttr(self.name, NotImplemented) != NotImplemented
        elif op == '=':
            return self.value == element.getAttr(self.name, NotImplemented)
        elif op == '~=':
            return self.value in element.getAttr(self.name, '').split()
        elif op == '|=':
            return self.value in element.getAttr(self.name, '').split('-')
        else:
            raise RuntimeError("Unknown operator %r for %r" % (self.op, self))

class CSSSelectorPseudoQualifier(CSSSelectorQualifierBase):
    def __init__(self, attrName, params=()):
        self.name = attrName
        self.params = tuple(params)
    def isPseudo(self): 
        return True
    def __hash__(self): 
        return hash((self.name, self.params))
    def asString(self): 
        if self.params:
            return ':'+self.name
        else:
            return ':%s(%s)' % (self.name, self.params)
    def matches(self, element): 
        return element.inPseudoState(self.name, self.params)

class CSSSelectorCombinationQualifier(CSSSelectorQualifierBase):
    def __init__(self, op, selector):
        self.op = op
        self.selector = selector 
    def isCombiner(self): 
        return True
    def __hash__(self): 
        return hash((self.op, self.selector))
    def asImmutable(self): 
        return self.__class__(self.op, self.selector.asImmutable())
    def asString(self): 
        return '%s%s' % (self.selector.asString(), self.op)
    def matches(self, element):
        op, selector = self.op, self.selector
        if op == ' ':
            for parent in element.iterXMLParents():
                if selector.matches(parent):
                    return True
            else: 
                return False
        elif op == '>':
            for parent in element.iterXMLParents():
                if selector.matches(parent):
                    return True
                else: 
                    return False
        elif op == '+':
            return selector.matches(element.getPreviousSibling())

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ CSS Misc
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CSSTerminalFunction(object):
    def __init__(self, name, params):
        self.name = name
        self.params = params

    def __repr__(self):
        return '<CSS function: %s(%s)>' % (self.name, ', '.join(self.params))

class CSSTerminalOperator(tuple):
    def __new__(klass, *args):
        return tuple.__new__(klass, args)

    def __repr__(self):
        return 'op' + tuple.__repr__(self)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ CSS Objects
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CSSDeclarations(dict):
    def copy(self):
        return self.__class__(self.iteritems())

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CSSRuleset(dict):
    def isRuleset(self): 
        return True
    def isDualRuleset(self): 
        return False

    def copy(self):
        result = self.__class__()
        for nodeFilter, declarations in self.iteritems():
            result[nodeFilter] = declarations.copy()

    def findAllCSSRulesFor(self, element):
        for nodeFilter, declarations in self.iteritems():
            if (nodeFilter.matches(element)):
                yield (nodeFilter, declarations)

    def findCSSRulesFor(self, element, attrName):
        ruleResults = []
        for nodeFilter, declarations in self.iteritems():
            if (attrName in declarations) and (nodeFilter.matches(element)):
                ruleResults.append((nodeFilter, declarations))
        ruleResults.sort()
        return ruleResults

    def findCSSRuleFor(self, element, attrName):
        # rule is packed in a list to differentiate from "no rule" vs "rule
        # whose value evalutates as False"
        return self.findCSSRulesFor(element, attrName)[-1:]

    def merge(self, ruleset):
        for rhsNodeFilter, rhsDelcarations in ruleset.iteritems():
            declarations = self.setdefault(rhsNodeFilter, rhsDelcarations)
            if declarations is not rhsDelcarations:
                declarations.update(rhsDelcarations)

class CSSInlineRuleset(CSSRuleset, CSSDeclarations):
    def copy(self):
        return self.__class__(self.iteritems())

    def findAllCSSRulesFor(self, element):
        yield (CSSInlineSelector(), self)

    def findCSSRulesFor(self, element, attrName):
        if attrName in self:
            return [(CSSInlineSelector(), self)]
        else: return []

    def findCSSRuleFor(self, element, attrName):
        # rule is packed in a list to differentiate from "no rule" vs "rule
        # whose value evalutates as False"
        return self.findCSSRulesFor(*args, **kw)[-1:]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CSSDualRuleset(object):
    """Combines important and non-important styles into a single ruleset"""
    RulesetFactory = CSSRuleset
    normal = None
    important = None

    def __init__(self, normalRuleset=None, importantRuleset=None):
        self.setRulesets(normalRuleset, importantRuleset)

    def __repr__(self):
        strArgs = (self.__class__.__name__, self.important, self.normal)
        return '<%s important:%r normal:%r>' % strArgs

    def __len__(self):
        return len(self.important) + len(self.normal)
    def copy(self):
        self.__class__(self.normal.copy(), self.important.copy())

    def values(self):
        return list(self.itervalues())
    def keys(self):
        return list(self.iterkeys())
    def items(self):
        return list(self.iteritems())
    def iterkeys(self):
        return itertools.chain(self.important.iterkeys(), self.normal.iterkeys())
    def itervalues(self):
        return itertools.chain(self.important.itervalues(), self.normal.itervalues())
    def iteritems(self):
        return itertools.chain(self.important.iteritems(), self.normal.iteritems())

    def __getitem__(self, key):
        if key in self.important:
            return self.important[key]
        else:
            return self.normal[key]

    def isRuleset(self): 
        return False
    def isDualRuleset(self): 
        return True

    def getRulesets(self):
        return self.normal, self.important
    def setRulesets(self, normalRuleset=None, importantRuleset=None):
        if normalRuleset is None:
            normalRuleset = self.RulesetFactory()
        elif not normalRuleset.isRuleset():
            raise ValueError("normalRuleset (%r) does not report to be a vaild ruleset" % (normalRuleset,))
        self.normal = normalRuleset

        if importantRuleset is None:
            importantRuleset = self.RulesetFactory()
        elif not importantRuleset.isRuleset():
            raise ValueError("importantRuleset (%r) does not report to be a vaild ruleset" % (importantRuleset,))
        self.important = importantRuleset

    def merge(self, dualRulesetOrNormal, orImportant=None):
        if dualRulesetOrNormal:
            if isinstance(dualRulesetOrNormal, dict):
                self.normal.merge(dualRulesetOrNormal)
            elif dualRulesetOrNormal.isDualRuleset():
                self.normal.merge(dualRulesetOrNormal.normal)
                self.important.merge(dualRulesetOrNormal.important)
            else:
                self.normal.merge(dualRulesetOrNormal)

        if orImportant:
            self.important.merge(orImportant)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def findAllCSSRulesFor(self, element):
        for rule in self.important.findAllCSSRulesFor(element):
            yield rule
        for rule in self.normal.findAllCSSRulesFor(element):
            yield rule

    def findCSSRulesFor(self, element, attrName):
        ruleResults = self.important.findCSSRulesFor(element, attrName)
        ruleResults += self.normal.findCSSRulesFor(element, attrName)
        return ruleResults

    def findCSSRuleFor(self, element, attrName):
        return (self.important.findCSSRuleFor(element, attrName) or 
                    self.normal.findCSSRuleFor(element, attrName))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ CSS Builder
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CSSBuilder(cssParser.CSSBuilderAbstract):
    RulesetFactory = CSSRuleset
    DualRulesetFactory = CSSDualRuleset
    InlineRulesetFactory = CSSInlineRuleset
    SelectorFactory = CSSMutableSelector
    MediumSetFactory = set
    DeclarationsFactory = CSSDeclarations
    TermFunctionFactory = CSSTerminalFunction
    TermOperatorFactory = CSSTerminalOperator
    xmlnsSynonyms = {}
    mediumSet = set()
    charset = None

    def __init__(self, mediumSet=mediumSet):
        self.setMediumSet(mediumSet)

    def isValidMedium(self, filterMediums, default=True):
        if not filterMediums:
            return default
        if 'all' in filterMediums:
            return True

        filterMediums = self.MediumSetFactory(filterMediums)
        return bool(self.getMediumSet().intersection(filterMediums))

    def getMediumSet(self):
        return self.mediumSet
    def setMediumSet(self, mediumSet):
        self.mediumSet = self.MediumSetFactory(mediumSet)
    def updateMediumSet(self, mediumSet):
        self.getMediumSet().update(mediumSet)

    #~ helpers ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _pushState(self):
        _restoreState = self.__dict__
        self.__dict__ = self.__dict__.copy()
        self._restoreState = _restoreState
        self.namespaces = {}
    def _popState(self):
        self.__dict__ = self._restoreState

    def _declarations(self, declarations, DeclarationsFactory=None):
        DeclarationsFactory = DeclarationsFactory or self.DeclarationsFactory

        normal, important = [], []
        for d in declarations:
            if d[-1]:
                important.append(d[:-1])
            else: normal.append(d[:-1])
        return DeclarationsFactory(normal), DeclarationsFactory(important)

    def _xmlnsGetSynonym(self, uri):
        # Don't forget to substitute our namespace synonyms!
        return self.xmlnsSynonyms.get(uri or None, uri) or None

    #~ css results ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def beginStylesheet(self, context):
        self._pushState()

    def endStylesheet(self, context):
        self._popState()

    def stylesheet(self, stylesheetElements, stylesheetImports):
        result = self.DualRulesetFactory()

        for stylesheet in stylesheetImports:
            result.merge(stylesheet)
        for stylesheet in stylesheetElements:
            result.merge(stylesheet)
        return result

    def beginInline(self, context):
        self._pushState()

    def endInline(self, context):
        self._popState()

    def inline(self, declarations):
        normal, important = self._declarations(declarations, self.InlineRulesetFactory)
        normal.merge(important)
        return normal

    def ruleset(self, selectors, declarations):
        # Make sure to save copies of the declarations everywhere to prepare
        # for when the values are merged in self.stylesheet

        normalDecl, importantDecl = self._declarations(declarations)
        result = self.DualRulesetFactory()

        for s in selectors:
            s = s.asImmutable()
            if normalDecl:
                result.normal[s] = normalDecl.copy() 
            if importantDecl:
                result.important[s] = importantDecl.copy()
        return result

    #~ css namespaces ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def resolveNamespacePrefix(self, nsPrefix, name):
        if nsPrefix == '*':
            return (nsPrefix, '*', name)
        xmlns = self.namespaces.get(nsPrefix, None)
        xmlns = self._xmlnsGetSynonym(xmlns)
        return (nsPrefix, xmlns, name)

    #~ css @ directives ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def atCharset(self, charset):
        self.charset = charset

    def atImport(self, import_, filterMediums, cssParser):
        if self.isValidMedium(filterMediums, True):
            return cssParser.parseExternal(import_, self)
        return None

    def atNamespace(self, nsprefix, uri):
        self.namespaces[nsprefix] = uri

    def atMedia(self, filterMediums, rulesets):
        if self.isValidMedium(filterMediums, False):
            return rulesets
        else: 
            return None

    def atPage(self, page, pseudoPage, properties, margins):
        return [self.ruleset([self.selector('*')], properties)]

    def atPageMargin(self, page, pseudoPage, marginName, properties):
        return (marginName, self.ruleset([self.selector('*')], properties))

    def atFontFace(self, declarations):
        return [self.ruleset([self.selector('*')], declarations)]

    #~ css selectors ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def selector(self, name):
        return self.SelectorFactory(name)

    def combineSelectors(self, selectorA, op, selectorB):
        return self.SelectorFactory.combineSelectors(selectorA, op, selectorB)

    #~ css declarations ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def property(self, name, value, important=False):
        if value is not NotImplemented:
            return (name, value, important)

    def combineTerms(self, termA, op, termB):
        if op in (',', ' '):
            if isinstance(termA, list):
                termA.append(termB)
                return termA
            else:
                return [termA, termB]
        elif op is None and termB is None:
            return [termA]
        else:
            if isinstance(termA, list):
                # Bind these "closer" than the list operators -- i.e. work on
                # the (recursively) last element of the list
                termA[-1] = self.combineTerms(termA[-1], op, termB)
                return termA
            else:
                return self.TermOperatorFactory(termA, op, termB)

    def termIdent(self, value):
        return value

    def termNumber(self, value, units=None):
        if units:
            return value, units
        else:
            return value

    def termColor(self, value):
        return value

    def termURI(self, value):
        return value

    def termString(self, value):
        return value

    def termUnicodeRange(self, value):
        return value

    def termFunction(self, name, value):
        return self.TermFunctionFactory(name, value)

    def termUnknown(self, src): 
        return src, NotImplemented

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ CSS Parser -- finally!
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CSSParser(cssParser.CSSParser):
    CSSBuilderFactory = CSSBuilder

    def __init__(self, cssBuilder=None, create=True, **kw):
        if not cssBuilder and create:
            assert cssBuilder is None
            cssBuilder = self.createCSSBuilder(**kw)
        cssParser.CSSParser.__init__(self, cssBuilder)

    def createCSSBuilder(self, **kw):
        return self.CSSBuilderFactory(**kw)

    def parseExternal(self, cssResourceName, cssBuilder):
        if os.path.isfile(cssResourceName):
            cssFile = file(cssResourceName, 'r')
            return self.parseFile(cssFile, True)
        else:
            raise RuntimeError("Cannot resolve external CSS file: \"%s\"" % cssResourceName)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Convience functions
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class _CSSNamespace(object):
    CSSParserFactory = CSSParser
    _defaultParser = None

    def _getDefaultParser(klass):
        if klass._defaultParser is None:
            klass._defaultParser = klass.CSSParserFactory()
        return klass._defaultParser
    _getDefaultParser = classmethod(_getDefaultParser)

    def updateNamespace(klass, ns):
        ns['parse'] = klass.parse
        ns['parseFile'] = klass.parseFile
        ns['parseInline'] = klass.parseInline
        ns['parseAttributes'] = klass.parseAttributes
        ns['parseSingleAttr'] = klass.parseSingleAttr
    updateNamespace = classmethod(updateNamespace)

    def parse(klass, src, context=None):
        return klass._getDefaultParser().parse(src, context)
    parse = classmethod(parse)

    def parseFile(klass, srcFile, context=None, closeFile=False):
        return klass._getDefaultParser().parseFile(srcFile, context, closeFile)
    parseFile = classmethod(parseFile)

    def parseInline(klass, src, context=None):
        return klass._getDefaultParser().parseInline(src, context)
    parseInline = classmethod(parseInline)

    def parseAttributes(klass, attributes={}, context=None, **kwAttributes):
        return klass._getDefaultParser().parseAttributes(attributes, context, **kwAttributes)
    parseAttributes = classmethod(parseAttributes)

    def parseSingleAttr(klass, attrValue):
        return klass._getDefaultParser().parseSingleAttr(attrValue)
    parseSingleAttr = classmethod(parseSingleAttr)

_CSSNamespace.updateNamespace(locals())

