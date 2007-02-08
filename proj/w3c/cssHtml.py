##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~ Copyright (C) 2002-2005  TechGame Networks, LLC.              ##
##~                                                               ##
##~ This library is free software; you can redistribute it        ##
##~ and/or modify it under the terms of the BSD style License as  ##
##~ found in the LICENSE file included with this distribution.    ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from css import *

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CSSCascadeStrategyForHTML(CSSCascadeStrategy):
    def _normalizeAttrNames(self, attrNames):
        if isinstance(attrNames, (str, unicode)):
            return attrNames.lower()
        else:
            return [n.lower() for n in attrNames]

class CSSBuilderForHTML(CSSBuilder):
    def property(self, name, value, important=False):
        name = name.lower()
        return CSSBuilder.property(self, name, value, important)

    def selector(self, name):
        name = name.lower()
        return CSSBuilder.selector(self, name)


class CSSParserForHTML(cssParser.CSSParser):
    CSSBuilderFactory = CSSBuilderForHTML


# Override the imports from the css namespace
CSSCascade = CSSCascadeStrategyForHTML
CSSBuilder = CSSBuilderForHTML
CSSParser = CSSParserForHTML

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Convience functions
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class _CSSNamespaceForHtml(_CSSNamespace):
    CSSParserFactory = CSSParserForHTML

_CSSNamespaceForHtml.updateNamespace(locals())

