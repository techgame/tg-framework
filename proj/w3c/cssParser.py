#!/usr/bin/env python
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##~ Copyright (C) 2002-2004  TechGame Networks, LLC.
##~ 
##~ This library is free software; you can redistribute it and/or
##~ modify it under the terms of the BSD style License as found in the 
##~ LICENSE file included with this distribution.
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""CSS-2.1 parser, with CSS 3 enhanced page parsing (compatible with CSS-2.1).

The CSS 2.1 Specification from which this parser was derived can be found at 
http://www.w3.org/TR/CSS21/

The CSS 3 Paged Media Module from which enhancements to this parser were 
derived can be found at http://www.w3.org/TR/css3-page/

Primary Classes:
    * CSSParser
        Parses CSS source forms into results using a Builder Pattern.  Must
        provide concrete implemenation of CSSBuilderAbstract.

    * CSSBuilderAbstract
        Outlines the interface between CSSParser and it's rule-builder.
        Compose CSSParser with a concrete implementation of the builder to get
        usable results from the CSS parser.

Dependencies: 
    python 2.3 (or greater)
    re

Credits:
    * 2005.07.12 Andre Soereng
        http://www.w3.org/TR/CSS21/syndata.html#parsing-errors    
    
    * 2005.03.23 Gary Poster
        Host of bugfixes and testing of the engine.  He also added support for
        page margins from http://www.w3.org/TR/css3-page/

    * 2005.04.06 Fred Drake
        Bugfix and test for ticket:43 and ticket:44
        
    * 2005.04.15 Henning Ramm
        Lots of good documentation for the CSSParser various parse functions,
        which inspired more thorough documentation of the interfaces.
"""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import re

try: 
    set
except NameError:
    from sets import Set as set

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CSSSelectorAbstract(object):
    """Outlines the interface between CSSParser and its rule-builder for selectors.

    CSSBuilderAbstract.selector and CSSBuilderAbstract.combineSelectors must
    return concrete implementations of this abstract.

    See css.CSSMutableSelector for an example implementation.
    """

    def addHashId(self, hashId): 
        """Modify the selector to respond to hashId.  
        
        #hashId {...}

        HashId is a string."""
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def addClass(self, className): 
        """Modify the selector to respond to className classes.
        
        .className {...}

        className is a string."""
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def addAttribute(self, attrName): 
        """Modify the selector to respond to objects with an attrName attribute.
        
        [attrName] {...}

        attrName is a string."""
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def addAttributeOperation(self, attrName, attrOp, attrValue): 
        """Modify the selector to respond to objects with an attrName attribute
        related to attrValue by attrOp.
        
        [attrName] {...}

        attrName and attrValue are strings.
        attrOp is one of '=', '~=', '|=', '&=', '^=', '!=', '<>'
        """
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def addPseudo(self, pseudo): 
        """Modify the selector to respond to pseudo-classes.

        :pseudo {...}

        pseudo is a string."""
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def addPseudoFunction(self, pseudoFn, value): 
        """Modify the selector to respond to pseudo-class functions.

        :pseudoFn(value) {...}

        pseudoFn and value are strings."""
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

class CSSBuilderAbstract(object):
    """Outlines the interface between CSSParser and its rule-builder.  
    
    Compose CSSParser with a concrete implementation of the builder to get
    usable results from the CSS parser.

    See css.CSSBuilder for an example implementation
    """

    #~ css results ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def beginStylesheet(self, context): 
        """Called at the beginning of a full stylesheet parse.
        
        Context is simply passed through the parser to the builder"""
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def stylesheet(self, rulesets, imports): 
        """Should return a stylesheet suitable for the subclass.  

        Rulesets is a list of results from ruleset() and @directives from at*()
        methods.  Imports is a list of imports returned from atImport()."""
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def endStylesheet(self, context): 
        """Called at the end of a full stylesheet parse.
        
        Context is simply passed through the parser to the builder"""
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

    def beginInline(self, context): 
        """Called at the beginning of an inline stylesheet parse.

        Context is simply passed through the parser to the builder"""
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def inline(self, declarations): 
        """Should return an inline declaration result suitable for the subclass.  

        Declarations is a list of properties returned by property()."""
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def endInline(self, context): 
        """Called at the end of an inline stylesheet parse.

        Context is simply passed through the parser to the builder"""
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

    def ruleset(self, selectors, declarations): 
        """Should return the ruleset suitable for the subclass.  
        
        Selectors is a list of selectors returned by either selector() or
        combineSelectors().  Delcarations is a list of properties returned by
        property().
        """
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

    #~ css namespaces ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def resolveNamespacePrefix(self, nsPrefix, name): 
        """Should return a single name correlating to the namespace prefix and
        the name.  This affects the name passed to termIdent(), selector(),
        and CSSSelectorAbstract's addAttribute() and addAttributeOperation().

        See atNamespace and the CSS spec.
        """
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

    #~ css @ directives ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def atCharset(self, charset): 
        """Charset is a string from the @charset directive"""
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def atImport(self, import_, filterMediums, cssParser): 
        """Should return the result of importing 'import_' reference string if
        the current medium matches the filterMediums.  An implementation may
        choose to return a callback for this method instead.  The list of
        results from this method are passed to stylehseet()
        
        cssParser is an instance implementation of CSSParser"""
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def atNamespace(self, nsPrefix, uri): 
        """Called for each @namespace directive to inform the builder of nsPrefix's associated url."""
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def atMedia(self, filterMediums, rulesets): 
        """Should return rulesets if current medium matches the filterMediums.
        rulesets is a list of results from ruleset()"""
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def atPage(self, page, pseudoPage, declarations, margins): 
        """Should return a list of rulesets (possibly empty) to be passed to stylesheet().

        Page and PseudoPage are strings.  Declarations is a list of properties.
        Margins is a list of results from atPageMargin().  

        See atPageMargin() and the extended `CSS 3 candidate recommendation`__

        .. __: http://www.w3.org/TR/css3-page/
        """
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def atPageMargin(self, page, pseudoPage, marginName, declarations):
        """Should return a margin result suitable for atPage()'s margins argument.

        Page, PseudoPage, and MarginName are strings.  Declarations is a
        list of properties.

        See atPage() and the extended `CSS 3 candidate recommendation`__

        .. __: http://www.w3.org/TR/css3-page/
        """
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def atFontFace(self, declarations): 
        """Parses an @font-face directive.  Should return a list of rulesets to
        be passed to stylesheet()."""
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

    #~ css selectors ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def combineSelectors(self, selectorA, combiner, selectorB): 
        """Should combine a selector suitable to the subclass implementation.
        Combiner is typically one of " ", "+", or ">".  Please see the CSS spec
        for definition of these combiners.  
        
        The result must implement CSSSelectorAbstract"""
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def selector(self, name): 
        """Should return a selector suitable to the subclass implementation.

        The result must implement CSSSelectorAbstract"""
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

    #~ css declarations ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def property(self, name, value, important=False): 
        """Should return what the subclass defines as a property binding of
        name, value and importance.
        
        Name is a string, value is the result of either a term*() or
        combineTerms() methods."""
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def combineTerms(self, termA, combiner, termB): 
        """Needs to return the appropriate combination result of termA and
        termB using combiner.  Combiner is usually one of '/', '+', ',' and the
        terms are results from the term*() methods provided here. """
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def termIdent(self, value): 
        """Should return what the subclass defines as an ident terminal.
        Value is a string."""
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def termNumber(self, value, units=None): 
        """Should return what the subclass defines as a number terminal
        Value and unites are strings."""
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def termColor(self, value): 
        """Should return what the subclass defines as a color terminal
        Value is a string."""
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def termURI(self, value): 
        """Should return what the subclass defines as a URI terminal
        Value is a string."""
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def termString(self, value): 
        """Should return what the subclass defines as a string terminal
        Value is a string."""
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def termUnicodeRange(self, value): 
        """Should return what the subclass defines as a unicode range terminal
        Value is a string."""
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def termFunction(self, name, value): 
        """Should return what the subclass defines as a function terminal
        Name and value are strings."""
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def termUnknown(self, src): 
        """Should return what the subclass decides to do with an unknown terminal
        Src is a string."""
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ CSS Parser
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CSSParseError(Exception): 
    src = None
    fullsrc = None
    inline = False
    _baseSrcRef = ('<unknown>', 1)

    def __init__(self, msg, src):
        Exception.__init__(self, msg)
        self.src = src

    def __str__(self):
        return '%s (%s)' % (Exception.__str__(self), self.getSrcRefString())

    def setFullCSSSource(self, fullsrc, inline=False):
        self.fullsrc = fullsrc
        if inline:
            self.inline = inline

    def _getFullSrcIndex(self):
        return len(self.fullsrc) - len(self.src)

    def getLineSrc(self):
        lineIdx = 1 + self.fullsrc.rfind('\n', 0, self._getFullSrcIndex())
        lineSrc = self.fullsrc[lineIdx:].split('\n', 1)[0]
        return lineSrc

    def getLine(self):
        return self._getLineOffset() + self.fullsrc.count('\n', 0, self._getFullSrcIndex())

    def getColumn(self):
        linesrc = self.getLineSrc()
        return linesrc.index(self.src.split('\n', 1)[0]) + 1

    def getSrcRef(self):
        return (self.getFilename(), self.getLine())
    def getBaseSrcRef(self, srcRef):
        return self._baseSrcRef
    def setBaseSrcRef(self, srcRef):
        self._baseSrcRef = srcRef

    def getFilename(self):
        return self._baseSrcRef[0]
    def setFilename(self, filename):
        self._baseSrcRef = (filename, 1)
    def _getLineOffset(self):
        return self._baseSrcRef[1]

    def getSrcRefString(self):
        return '\"%s\" line: %d col: %d' % (self.getFilename(), self.getLine(), self.getColumn())

    def raiseFromSrc(self, srcref=None):
        from TG.introspection.stack import traceSrcrefExec
        if srcref is not None:
            self.setBaseSrcRef(srcref)
        traceSrcrefExec(self.getSrcRef(), 'raise cssError', cssError=self)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CSSParser(object):
    """CSS-2.1 parser dependent only upon the re module.
    
    Implemented directly from http://www.w3.org/TR/CSS21/grammar.html
    Tested with some existing CSS stylesheets for portability.
    
    CSS Parsing API:
        * setCSSBuilder() 
            To set a concrete instance implementing CSSBuilderAbstract

        * parseFile()
            Use to parse external stylesheets using a file-like object

            >>> cssFile = open('test.css', 'r')
            >>> stylesheets = myCSSParser.parseFile(cssFile)

        * parse()
            Use to parse embedded stylesheets using source string

            >>> cssSrc = '''
            ... body,body.body {
            ...     font: 110%, "Times New Roman", Arial, Verdana, Helvetica, serif;
            ...     background: White;
            ...     color: Black;
            ... }
            ... a {text-decoration: underline;}
            ... '''
            >>> stylesheets = myCSSParser.parse(cssSrc)

        * parseInline()
            Use to parse inline stylesheets using attribute source string

            >>> style = 'font: 110%, "Times New Roman", Arial, Verdana, Helvetica, serif; background: White; color: Black'
            >>> stylesheets = myCSSParser.parseInline(style)

        * parseAttributes()
            Use to parse attribute string values into inline stylesheets

            >>> stylesheets = myCSSParser.parseAttributes(
            ...     font='110%, "Times New Roman", Arial, Verdana, Helvetica, serif',
            ...     background='White',
            ...     color='Black')

        * parseSingleAttr()
            Use to parse a single string value into a CSS expression

            >>> fontValue = myCSSParser.parseSingleAttr('110%, "Times New Roman", Arial, Verdana, Helvetica, serif')
    """

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    ParseError = CSSParseError
    bParseStrict = False

    AttributeOperators = set(('=', '~=', '|=', '&=', '^=', '!=', '<>'))
    SelectorQualifiers = set(('#', '.', '[', ':'))
    SelectorCombiners = set(('+', '>'))
    ExpressionOperators = set(('/', '+', ','))
    DeclarationSetters = set((':', '='))
    DeclarationBoundry = set(('', ',', '{','}', '[',']','(',')'))

    # atKeywordHandlers is a class-level dictionary to enable extending
    # @-directives in a standard way.  See _parseAtKeyword for details.
    atKeywordHandlers = {} 

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Regular expressions
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    if True: # makes the following code foldable
        _orRule = lambda *args: '|'.join(args)
        _reflags = re.I | re.M | re.U
        i_hex = '[0-9a-fA-F]'
        i_nonascii = u'[\200-\377]'
        i_unicode = '\\\\(?:%s){1,6}\s?' % i_hex
        i_escape = _orRule(i_unicode, u'\\\\[ -~\200-\377]')
        i_nmstart = _orRule('[-A-Za-z_]', i_nonascii, i_escape)
        i_nmchar = _orRule('[-0-9A-Za-z_]', i_nonascii, i_escape)
        i_ident = '((?:%s)(?:%s)*)' % (i_nmstart,i_nmchar)
        re_ident = re.compile(i_ident, _reflags)
        i_element_name = '((?:%s)|\*)' % (i_ident[1:-1],)
        re_element_name = re.compile(i_element_name, _reflags)
        i_namespace_selector = '((?:%s)|\*|)\|(?!=)' % (i_ident[1:-1],)
        re_namespace_selector = re.compile(i_namespace_selector, _reflags)
        i_class = '\\.' + i_ident
        re_class = re.compile(i_class, _reflags)
        i_hash = '#((?:%s)+)' % i_nmchar
        re_hash = re.compile(i_hash, _reflags)
        i_rgbcolor = '(#%s{6}|#%s{3})' % (i_hex, i_hex)
        re_rgbcolor = re.compile(i_rgbcolor, _reflags)
        i_nl = u'\n|\r\n|\r|\f'
        i_escape_nl = u'\\\\(?:%s)' % i_nl
        i_string_content = _orRule(u'[\t !#$%&(-~]', i_escape_nl, i_nonascii, i_escape)
        i_string1 = u'\"((?:%s|\')*)\"' % i_string_content
        i_string2 = u'\'((?:%s|\")*)\'' % i_string_content
        i_string = _orRule(i_string1, i_string2)
        re_string = re.compile(i_string, _reflags)

        i_string1_unexpectedEnd = i_string1[:-1]
        i_string2_unexpectedEnd = i_string2[:-1]
        i_string_unexpectedEnd = _orRule(i_string1_unexpectedEnd, i_string2_unexpectedEnd)
        re_string_unexpectedEnd = re.compile(i_string_unexpectedEnd, _reflags)

        i_uri = (u'url\\(\s*(?:(?:%s)|((?:%s)+))\s*\\)'
                 % (i_string, _orRule('[!#$%&*-~]', i_nonascii, i_escape)))
        re_uri = re.compile(i_uri, _reflags)
        i_num = u'([-+]?[0-9]+(?:\\.[0-9]+)?)|([-+]?\\.[0-9]+)'
        re_num = re.compile(i_num, _reflags)
        i_unit = '(%%|%s)?' % i_ident
        re_unit = re.compile(i_unit, _reflags)
        i_function = i_ident + '\\(' 
        re_function = re.compile(i_function, _reflags)
        i_functionterm = u'[-+]?' + i_function
        re_functionterm = re.compile(i_functionterm, _reflags)
        i_unicoderange1 = "(?:U\\+%s{1,6}-%s{1,6})" % (i_hex, i_hex)
        i_unicoderange2 = "(?:U\\+\?{1,6}|{h}(\?{0,5}|{h}(\?{0,4}|{h}(\?{0,3}|{h}(\?{0,2}|{h}(\??|{h}))))))"
        i_unicoderange = i_unicoderange1 # u'(%s|%s)' % (i_unicoderange1, i_unicoderange2)
        re_unicoderange = re.compile(i_unicoderange, _reflags)
        i_important = u'!\s*(important)'
        re_important = re.compile(i_important, _reflags)

        i_comment = u'\\s*(?:\\s*\\/\\*[^*]*\\*+([^/*][^*]*\\*+)*\\/\\s*)*'
        re_comment = re.compile(i_comment, _reflags)

        i_declarationError = u'((?:[^;{}]*(?:{[^}]*})?)*)'
        re_declarationError = re.compile(i_declarationError, _reflags)

        i_atKeywordErrorStart = u'([^;{]*[;{])'
        re_atKeywordErrorStart = re.compile(i_atKeywordErrorStart, _reflags)
        i_atKeywordErrorGroup = u'([^{}]*[{}])'
        re_atKeywordErrorGroup = re.compile(i_atKeywordErrorGroup, _reflags)

        del _orRule

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __init__(self, cssBuilder=None):
        self.setCSSBuilder(cssBuilder)
        
    #~ CSS Builder to delegate to ~~~~~~~~~~~~~~~~~~~~~~~~

    def getCSSBuilder(self):
        """A concrete instance implementing CSSBuilderAbstract"""
        return self._cssBuilder
    def setCSSBuilder(self, cssBuilder):
        """A concrete instance implementing CSSBuilderAbstract"""
        self._cssBuilder = cssBuilder
    cssBuilder = property(getCSSBuilder, setCSSBuilder)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public CSS Parsing API
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def parseFile(self, srcFile, context=None, closeFile=False):
        """Parses CSS file-like objects using the current cssBuilder.
        Use for external stylesheets.

            >>> cssFile = open('test.css', 'r')
            >>> stylesheets = myCSSParser.parseFile(cssFile)

        Context is a pass-through variable to the CSSBuilder.
        """

        try:
            result = self.parse(srcFile.read(), context)
        finally:
            if closeFile:
                srcFile.close()
        return result

    def parse(self, src, context=None):
        """Parses CSS string source using the current cssBuilder.  
        Use for embedded stylesheets.

            >>> cssSrc = '''
                body,body.body {
                    font: 110%, "Times New Roman", Arial, Verdana, Helvetica, serif;
                    background: White;
                    color: Black;
                }
                a {text-decoration: underline;}
            '''
            >>> stylesheets = myCSSParser.parse(cssSrc)
        
        Context is just a pass-through variable to the CSSBuilder.
        """

        self.cssBuilder.beginStylesheet(context)
        try:
            try:
                src, stylesheet = self._parseStylesheet(src)
            except self.ParseError, err:
                err.setFullCSSSource(src)
                raise
        finally:
            self.cssBuilder.endStylesheet(context)
        return stylesheet

    def parseInline(self, src, context=None):
        """Parses CSS inline source string using the current cssBuilder.
        Use to parse inline stylesheets using attribute source string
        Use to parse a tag's 'sytle'-like attribute.

            >>> style = 'font: 110%, "Times New Roman", Arial, Verdana, Helvetica, serif; background: White; color: Black'
            >>> stylesheets = myCSSParser.parseInline(style)

        Context is just a pass-through variable to the CSSBuilder.
        """

        self.cssBuilder.beginInline(context)
        try:
            try:
                src, declarations = self._parseDeclarationGroup(self._stripCSS(src), braces=False)
            except self.ParseError, err:
                err.setFullCSSSource(src, inline=True)
                raise

            result = self.cssBuilder.inline(declarations)
        finally:
            self.cssBuilder.endInline(context)
        return result

    def parseAttributes(self, attributes={}, context=None, **kwAttributes):
        """Parses CSS attribute source strings and return an inline stylesheet.
        Use to parse a tag's highly CSS-based attributes like 'font'.

        Use to parse attribute string values into inline stylesheets

            >>> stylesheets = myCSSParser.parseAttributes(
                    font='110%, "Times New Roman", Arial, Verdana, Helvetica, serif',
                    background='White',
                    color='Black')

        Context is just a pass-through variable to the CSSBuilder.

        See also: parseSingleAttr
        """
        if attributes:
            kwAttributes.update(attributes)

        self.cssBuilder.beginInline(context)
        try:
            properties = []
            try:
                for propertyName, src in kwAttributes.iteritems():
                    src, property = self._parseDeclarationProperty(self._stripCSS(src), propertyName)
                    if property is not None:
                        properties.append(property)

            except self.ParseError, err:
                err.setFullCSSSource(src, inline=True)
                raise

            result = self.cssBuilder.inline(properties)
        finally:
            self.cssBuilder.endInline(context)
        return result

    def parseSingleAttr(self, attrValue):
        """Parse a single CSS attribute source string and return the built CSS expression.
        Use to parse a tag's highly CSS-based attributes like 'font'.
        Use to parse a single string value into a CSS expression

            >>> fontValue = myCSSParser.parseSingleAttr('110%, "Times New Roman", Arial, Verdana, Helvetica, serif')


        See also: parseAttributes
        """

        attributes = self.parseAttributes(singleAttr=attrValue)
        return attributes['singleAttr']

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Internal _parse methods
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _parseStylesheet(self, src):
        """Parses a CSS stylesheet into imports and rulesets, returning the
        result of cssBuilder.stylesheet()
        
        ::
            stylesheet
                : [ CHARSET_SYM S* STRING S* ';' ]?
                    [S|CDO|CDC]* [ import [S|CDO|CDC]* ]*
                    [ [ ruleset | media | page | font_face ] [S|CDO|CDC]* ]*
                ;
        """
        # [ CHARSET_SYM S* STRING S* ';' ]?
        src = self._parseAtCharset(src)

        # [S|CDO|CDC]*
        src = self._parseSCDOCDC(src)
        #  [ import [S|CDO|CDC]* ]*
        src, imports = self._parseAtImports(src)

        # [ namespace [S|CDO|CDC]* ]*
        src = self._parseAtNamespace(src)

        rulesets = []

        # [ [ ruleset | atkeywords ] [S|CDO|CDC]* ]*
        while src: # due to ending with ]*
            if src.startswith('@'):
                # @media, @page, @font-face
                src, atResults = self._parseAtKeyword(src)
                if atResults is not None:
                    rulesets.extend(atResults)
            else:
                # ruleset
                src, ruleset = self._parseRuleset(src)
                rulesets.append(ruleset)

            # [S|CDO|CDC]*
            src = self._parseSCDOCDC(src)

        stylesheet = self.cssBuilder.stylesheet(rulesets, imports)
        return src, stylesheet

    def _parseSCDOCDC(self, src):
        """[S|CDO|CDC]*"""
        while 1:
            src = self._stripCSS(src)
            if src.startswith('<!--'):
                src = src[4:]
            elif src.startswith('-->'):
                src = src[3:]
            else: 
                break
        return src

    #~ CSS @ directives ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _parseAtCharset(self, src):
        """Parses @charset directives.

        ::
            [ CHARSET_SYM S* STRING S* ';' ]?
        """
        if src.startswith('@charset '):
            src = self._stripCSS(src[9:])
            src, charset = self._getString(src)
            src = self._stripCSS(src)
            if src[:1] != ';':
                raise self.ParseError('@charset expected a terminating \';\'', src)
            src = self._stripCSS(src[1:])

            self.cssBuilder.atCharset(charset)
        return src

    def _parseAtImports(self, src):
        """Returns a list of imports returned by cssBuilder.atImport().

        ::
            [ import [S|CDO|CDC]* ]*"""
        result = []
        while src.startswith('@import '):
            src = self._stripCSS(src[8:])

            src, import_ = self._getStringOrURI(src)
            if import_ is None:
                raise self.ParseError('Import expecting string or url', src)

            filterMediums = []
            src, medium = self._getIdent(self._stripCSS(src))
            while medium is not None:
                filterMediums.append(medium)
                if src[:1] == ',':
                    src = self._stripCSS(src[1:])
                    src, medium = self._getIdent(src)
                else: 
                    break

            if src[:1] != ';':
                raise self.ParseError('@import expected a terminating \';\'', src)
            src = self._stripCSS(src[1:])

            stylesheet = self.cssBuilder.atImport(import_, filterMediums, self)
            if stylesheet is not None:
                result.append(stylesheet)

            src = self._parseSCDOCDC(src)
        return src, result

    def _parseAtNamespace(self, src):
        """Parses @namespace directives.

        Calls cssBuilder.atNamespace for each directive.

        ::
            namespace : 
            @namespace S* [IDENT S*]? [STRING|URI] S* ';' S*
        """
        
        src = self._parseSCDOCDC(src)
        while src.startswith('@namespace'):
            src = self._stripCSS(src[len('@namespace'):])

            src, namespace = self._getStringOrURI(src)
            if namespace is None:
                src, nsPrefix = self._getIdent(src)
                if nsPrefix is None:
                    raise self.ParseError('@namespace expected an identifier or a URI', src)
                src, namespace = self._getStringOrURI(self._stripCSS(src))
                if namespace is None:
                    raise self.ParseError('@namespace expected a URI', src)
            else:
                nsPrefix = None

            src = self._stripCSS(src)
            if src[:1] != ';':
                raise self.ParseError('@namespace expected a terminating \';\'', src)
            src = self._stripCSS(src[1:])

            self.cssBuilder.atNamespace(nsPrefix, namespace)

            src = self._parseSCDOCDC(src)
        return src

    def _parseAtKeyword(self, src):
        """[media | page | font_face | unknown_keyword]"""
        if src.startswith('@'): 
            src = src[1:]
        else: 
            raise self.ParseError('atKeyword missing @ sign', src)

        src, atDirective = self._getIdent(src)
        src = self._stripCSS(src)

        directiveHandler = self.atKeywordHandlers.get(atDirective,
                                    self.__class__._parseAtUnknownHandler)
        return directiveHandler(self, atDirective, src)

    def _parseAtUnknownHandler(self, atDirective, src):
        if self.bParseStrict:
            raise self.ParseError('Unknown @-Directive \"%s\"' % atDirective, src)

        src, content = self._getMatchResult(self.re_atKeywordErrorStart, src)
        src = self._stripCSS(src)

        content = content.lstrip()
        if content[0] == '{': n = 1
        elif content[-1] == '{': n = 2
        else: n = 0

        while n:
            src, content = self._getMatchResult(self.re_atKeywordErrorGroup, src)
            src = self._stripCSS(src)
            n += {'{':1, '}':-1}.get(content[-1], 0)

        return src, []

    def _parseAtMedia(self, atDirective, src):
        """media
        : MEDIA_SYM S* medium [ ',' S* medium ]* '{' S* ruleset* '}' S*
        ;
        """
        filterMediums = []
        while src and src[0] != '{':
            src, medium = self._getIdent(src)
            if medium is None: 
                raise self.ParseError('@media rule expected media identifier', src)
            filterMediums.append(medium)
            if src[0] == ',':
                src = self._stripCSS(src[1:])
            else:
                src = self._stripCSS(src)

        if not src.startswith('{'):
            raise self.ParseError('Ruleset opening \'{\' not found', src)
        src = self._stripCSS(src[1:])
        
        rulesets = []
        while src and not src.startswith('}'):
            src, ruleset = self._parseRuleset(src)
            rulesets.append(ruleset)
            src = self._stripCSS(src)

        if not src.startswith('}'):
            if self.bParseStrict or src:
                raise self.ParseError('Ruleset closing \'}\' not found', src)
        elif src: 
            src = self._stripCSS(src[1:])

        result = self.cssBuilder.atMedia(filterMediums, rulesets)
        if result is None:
            result = []
        return src, result
    atKeywordHandlers['media'] = _parseAtMedia

    def _parseAtPage(self, atDirective, src):
        """@page directive.  Returns result from cssBuilder.atPage
        
        Supports extended CSS 3 candidate recommendation
        http://www.w3.org/TR/css3-page/
        
        ::
            @page
                : PAGE_SYM S* IDENT? pseudo_page? S*
                '{' S* [ declaration | @margin ] [ ';' 
                    S* [ declaration | @margin ]? ]* '}' S*
                ;
        """
        if not src.startswith('{'):
            src, page = self._getIdent(src)
        else: page = ''

        if src[:1] == ':':
            src, pseudoPage = self._getIdent(src[1:])
            src = src[1:]
        else: pseudoPage = ''
        src = self._stripCSS(src)

        if not src.startswith('{'):
            raise self.ParseError('Ruleset opening \'{\' not found', src)
        src = self._stripCSS(src[1:])

        declarations, margins = [], []
        while src[:1] not in self.DeclarationBoundry:
            # declaration group while loop.
            if src.startswith('@'):
                # @ specific margin
                src, margin = self._parseAtPageMargin(src[1:], page, pseudoPage)
                margins.append(margin)
            else:
                # declaration
                src, property = self._parseDeclaration(src)
                if property is not None:
                    declarations.append(property)

                if src.startswith(';'):
                    src = self._stripCSS(src[1:])

            # [S|CDO|CDC]*
            src = self._parseSCDOCDC(src)

        if not src.startswith('}'):
            raise self.ParseError('Ruleset closing \'}\' not found', src)
        else: 
            src = self._stripCSS(src[1:])

        result = self.cssBuilder.atPage(page, pseudoPage, declarations, margins)
        if result is None:
            result = []
        return self._stripCSS(src), result
    atKeywordHandlers['page'] = _parseAtPage

    def _parseAtPageMargin(self, src, page, pseudoPage):
        """@page margin directive.  Returns result from cssBuilder.atPageMargin
        
        Supports extended CSS 3 candidate recommendation
        http://www.w3.org/TR/css3-page/
        
        ::
            page margin
                : margin_sym S* '{' declaration [ ';' S* declaration? ]* '}' S*
                ;
        ;

        See _parseAtPage()
        """
        src, margin = self._getIdent(src)
        if margin is None:
            raise self.ParseError('At-margin rule received an unknown margin', src)
        src, declarations = self._parseDeclarationGroup(self._stripCSS(src))
        result = self.cssBuilder.atPageMargin(page, pseudoPage, margin.lower(), declarations)
        return src, result

    def _parseAtFontFace(self, atDirective, src):
        src, declarations = self._parseDeclarationGroup(src)
        result = self.cssBuilder.atFontFace(declarations)
        if result is None:
            result = []
        return src, result
    atKeywordHandlers['font-face'] = _parseAtFontFace

    #~ ruleset - see selector and declaration groups ~~~~

    def _parseRuleset(self, src):
        """Parses a CSS ruleset by parsing the selectors and declarations.
        Returns the result of cssBuilder.ruleset() from the list of selectors
        and list of declarations.
        
        ::
            ruleset
                : selector [ ',' S* selector ]*
                    '{' S* declaration [ ';' S* declaration ]* '}' S*
                ;
        """
        src, selectors = self._parseSelectorGroup(src)
        src, declarations = self._parseDeclarationGroup(self._stripCSS(src))
        result = self.cssBuilder.ruleset(selectors, declarations)
        return src, result

    #~ selector parsing ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _parseSelectorGroup(self, src):
        """Returns a list of selectors, complex or simple, returned from cssBuilder.selector().

        Each element must implement CSSSelectorAbstract."""
        selectors = []
        while src[:1] not in ('{','}', ']','(',')', ';', ''):
            src, selector = self._parseSelector(src)
            if selector is None:
                break
            selectors.append(selector)
            if src.startswith(','):
                src = self._stripCSS(src[1:])
        return src, selectors

    def _parseSelector(self, src):
        """Parses a complex selector.

        Selectors are combined using cssBuilder.combineSelectors() as necessary.
        Returns a modified selector from cssBuilder.selector() which must implement
        CSSSelectorAbstract.  

        ::
            selector
                : simple_selector [ combinator simple_selector ]*
                ;
        """
        src, selector = self._parseSimpleSelector(src)
        while src[:1] not in ('', ',', ';', '{','}', '[',']','(',')'):
            for combiner in self.SelectorCombiners:
                if src.startswith(combiner):
                    src = self._stripCSS(src[len(combiner):])
                    break
            else: 
                combiner = ' '
            src, selectorB = self._parseSimpleSelector(src)
            selector = self.cssBuilder.combineSelectors(selector, combiner, selectorB)
        return self._stripCSS(src), selector

    def _parseSimpleSelector(self, src):
        """Parses a single selector.  
        
        Complex selectors are handled by _parseSelector.  Returns a modified
        selector from cssBuilder.selector() which must implement
        CSSSelectorAbstract.

        ::
            simple_selector
                : [ namespace_selector ]? element_name? 
                [ HASH | class | attrib | pseudo ]* S*
                ;
        """
        src = self._stripCSS(src)
        src, nsPrefix = self._getMatchResult(self.re_namespace_selector, src)
        src = self._stripCSS(src)
        src, name = self._getMatchResult(self.re_element_name, src)
        src = self._stripCSS(src)
        if name: 
            pass # already *successfully* assigned
        elif src[:1] in self.SelectorQualifiers: 
            name = '*'
        else: 
            raise self.ParseError('Selector name or qualifier expected', src)

        name = self.cssBuilder.resolveNamespacePrefix(nsPrefix, name)
        selector = self.cssBuilder.selector(name)

        while src and src[:1] in self.SelectorQualifiers:
            src, hash_ = self._getMatchResult(self.re_hash, src)
            src = self._stripCSS(src)
            if hash_ is not None:
                selector.addHashId(hash_)
                continue

            src, class_ = self._getMatchResult(self.re_class, src)
            src = self._stripCSS(src)
            if class_ is not None:
                selector.addClass(class_)
                continue

            if src.startswith('['):
                src, selector = self._parseSelectorAttribute(src, selector)
            elif src.startswith(':'):
                src, selector = self._parseSelectorPseudo(src, selector)
            else: 
                break

        return self._stripCSS(src), selector

    def _parseSelectorAttribute(self, src, selector):
        """Parses a attribute selector.  

        Selector argument must implement CSSSelectorAbstract.
        Please see CSS spec for definition.
        
        ::
            attrib
                : '[' S* [ namespace_selector ]? IDENT S* 
                    [ [ '=' | INCLUDES | DASHMATCH ] S* [ IDENT | STRING ] S* ]? ']'
                ;
        """
        if not src.startswith('['):
            raise self.ParseError('Selector Attribute opening \'[\' not found', src)
        src = self._stripCSS(src[1:])

        src, nsPrefix = self._getMatchResult(self.re_namespace_selector, src)
        src = self._stripCSS(src)
        src, attrName = self._getIdent(src)

        if attrName is None:
            raise self.ParseError('Expected a selector attribute name', src)
        if nsPrefix is not None:
            attrName = self.cssBuilder.resolveNamespacePrefix(nsPrefix, attrName)

        for attrOp in self.AttributeOperators:
            if src.startswith(attrOp): 
                break
        else: 
            attrOp = ''
        src = self._stripCSS(src[len(attrOp):])

        if attrOp:
            src, attrValue = self._getIdent(src)
            if attrValue is None:
                src, attrValue = self._getString(src)
                if attrValue is None:
                    raise self.ParseError('Expected a selector attribute value', src)
        else: 
            attrValue = None

        if not src.startswith(']'):
            raise self.ParseError('Selector Attribute closing \']\' not found', src)
        else: 
            src = src[1:]

        if attrOp:
            selector.addAttributeOperation(attrName, attrOp, attrValue)
        else: 
            selector.addAttribute(attrName)
        return src, selector

    def _parseSelectorPseudo(self, src, selector):
        """Parses a pseudo selector.  

        Selector argument must implement CSSSelectorAbstract.
        Please see CSS spec for definition.

        ::
            pseudo
                : ':' [ IDENT | function ]
                ;
        """
        if not src.startswith(':'):
            raise self.ParseError('Selector Pseudo \':\' not found', src)
        src = src[1:]

        src, name = self._getIdent(src)
        if not name:
            raise self.ParseError('Selector Pseudo identifier not found', src)

        if src.startswith('('):
            # function
            src = self._stripCSS(src[1:])
            src, term = self._parseExpression(src, True)
            if not src.startswith(')'):
                raise self.ParseError('Selector Pseudo Function closing \')\' not found', src)
            src = src[1:]
            selector.addPseudoFunction(name, term)
        else:
            selector.addPseudo(name)

        return src, selector

    #~ declaration and expression parsing ~~~~~~~~~~~~~~~

    def _parseDeclarationGroup(self, src, braces=True):
        """Returns a list of properties returned from cssBuilder.property"""
        if src.startswith('{'): 
            src, braces = src[1:], True
        elif braces: 
            raise self.ParseError('Declaration group opening \'{\' not found', src)
        
        properties = []
        src = self._stripCSS(src)
        while src[:1] not in self.DeclarationBoundry:
            src, property = self._parseDeclaration(src)
            if property is not None: 
                properties.append(property)
            if src.startswith(';'):
                src = self._stripCSS(src[1:])

        if braces:
            if not src.startswith('}'):
                if self.bParseStrict or src:
                    raise self.ParseError('Declaration group closing \'}\' not found', src)
            src = src[1:]

        return self._stripCSS(src), properties

    def _parseDeclaration(self, src):
        """Returns a property or None.  
        
        Parses only the property name and the declaration setter.
        _parseDeclarationProperty completes the property by parsing the
        expression.
        
        :: 
            declaration
                : ident S* ':' S* expr prio?
                | /* empty */
        ;
        """
        # property
        src, propertyName = self._getIdent(src)
        property = None

        if propertyName is not None:
            src = self._stripCSS(src)
            # S* : S*
            if self.bParseStrict:
                if src[:1] != ':':
                    raise self.ParseError('Malformed declaration missing ":" before the value', src)
                src, property = self._parseDeclarationProperty(self._stripCSS(src[1:]), propertyName)

            elif src[:1] in self.DeclarationSetters:
                # Note: we are being fairly flexible here...  technically, the
                # ":" is *required*, but in the name of flexibility we support
                # an "=" transition
                src, property = self._parseDeclarationProperty(self._stripCSS(src[1:]), propertyName)

            else:
                # dump characters to next ; or }
                src, dumpText = self._getMatchResult(self.re_declarationError, src)
                src = self._stripCSS(src)
        elif self.bParseStrict:
            raise self.ParseError('Property name not present', src)

        return src, property

    def _parseDeclarationProperty(self, src, propertyName):
        """Returns the result from cssBuilder.property(), combining name and value for the declaration"""
        # expr
        src, expr = self._parseExpression(src)
        if expr is NotImplemented:
            return src, None

        # prio?
        src, important = self._getMatchResult(self.re_important, src)
        src = self._stripCSS(src)

        property = self.cssBuilder.property(propertyName, expr, important)
        return src, property

    def _parseExpression(self, src, returnList=False):
        """Returns the terms (combined if necessary) for the property's value expression.

        ::
            expr
            : term [ operator term ]*
            ;
        """
        src, term = self._parseExpressionTerm(src)

        if term is NotImplemented: 
            return src, term

        operator = None
        while src[:1] not in ('', ';', '{','}', '[',']', ')'):
            for operator in self.ExpressionOperators:
                if src.startswith(operator):
                    src = src[len(operator):]
                    break
            else: 
                operator = ' '
            src, term2 = self._parseExpressionTerm(self._stripCSS(src))
            if term2 is NotImplemented: 
                break
            else: 
                term = self.cssBuilder.combineTerms(term, operator, term2)

        if operator is None and returnList:
            term = self.cssBuilder.combineTerms(term, None, None)
            return src, term
        else:
            return src, term

    def _parseExpressionTerm(self, src):
        """Returns the result from the applicable cssBuilder.term*() method.

        ::
            term
            : unary_operator?  [ NUMBER S* | PERCENTAGE S* | LENGTH S* | EMS S*
                | EXS S* | ANGLE S* | TIME S* | FREQ S* | function ] | STRING S* 
                | IDENT S* | URI S* | RGB S* | UNICODERANGE S* | hexcolor
        ;
        """
        src, result = self._getMatchResult(self.re_num, src)
        if result is not None:
            src, units = self._getMatchResult(self.re_unit, src)
            term = self.cssBuilder.termNumber(result, units)
            return self._stripCSS(src), term

        src, result = self._getString(src, self.re_uri)
        if result is not None:
            term = self.cssBuilder.termURI(result)
            return self._stripCSS(src), term

        src, result = self._getString(src)
        if result is not None:
            term = self.cssBuilder.termString(result)
            return self._stripCSS(src), term

        src, result = self._getMatchResult(self.re_functionterm, src)
        if result is not None:
            src, params = self._parseExpression(src, True)
            if src[0] != ')':
                raise self.ParseError('Terminal function expression expected closing \')\'', src)
            src = self._stripCSS(src[1:])
            term = self.cssBuilder.termFunction(result, params)
            return src, term

        src, result = self._getMatchResult(self.re_rgbcolor, src)
        if result is not None:
            term = self.cssBuilder.termColor(result)
            return self._stripCSS(src), term

        src, result = self._getMatchResult(self.re_unicoderange, src)
        if result is not None:
            term = self.cssBuilder.termUnicodeRange(result)
            return self._stripCSS(src), term

        src, nsPrefix = self._getMatchResult(self.re_namespace_selector, src)
        src, result = self._getIdent(src)
        if result is not None:
            if nsPrefix is not None:
                result = self.cssBuilder.resolveNamespacePrefix(nsPrefix, result)
            term = self.cssBuilder.termIdent(result)
            return self._stripCSS(src), term

        src2, result = self._getString(src, self.re_string_unexpectedEnd)
        if result:
            if self.bParseStrict:
                raise self.ParseError('Unexpected end of string literal', src)

            src2 = self._stripCSS(src2)
            if not src2:
                # Special case where the CSS file was truncated, and we
                # should actually return the unterminated string
                term = self.cssBuilder.termString(result)
            else: 
                # Per section 4.2 of the CSS21 spec, unterminated strings
                # should be ignored
                term = NotImplemented
            return src2, term

        if self.bParseStrict:
            raise self.ParseError('Malformed declaration missing value', src)
        else:
            return self.cssBuilder.termUnknown(src)

    #~ utility methods ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def _getIdent(self, src, default=None):
        return self._getMatchResult(self.re_ident, src, default)

    def _getString(self, src, rexpression=None, default=None):
        if rexpression is None:
            rexpression = self.re_string
        result = rexpression.match(src)

        if result:
            strres = filter(None, result.groups())
            if strres:
                strres = strres[0]
            else:
                strres = ''
            return src[result.end():], strres 
        else: 
            return src, default

    def _getStringOrURI(self, src):
        src, result = self._getString(src, self.re_uri)
        if result is None:
            src, result = self._getString(src)
        return src, result

    def _getMatchResult(self, rexpression, src, default=None, group=1):
        result = rexpression.match(src)
        if result:
            return src[result.end():], result.group(group)
        else: 
            return src, default

    def _stripCSS(self, src):
        # Get rid of the comments
        match = self.re_comment.match(src)
        return src[match.end():]

