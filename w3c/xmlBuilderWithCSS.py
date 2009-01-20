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
import platform
import sets

import css
import xmlBuilder

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class XMLBuilderCSSMixin(object):
    cssDefaultMediumSet = None
    CSSParserFactory = css.CSSParser

    #~ CSS Related ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getCSSParser(self):
        if not hasattr(self, '_cssParser'):
            self._setupCSSParser()
        return self._cssParser
    def setCSSParser(self, cssParser):
        self._cssParser = cssParser
    cssParser = property(getCSSParser, setCSSParser)

    def _setupCSSParser(self):
        cssParser = self.CSSParserFactory(mediumSet=self.getCSSDefaultMediumSet())
        cssParser.setXMLBuilder(self)
        self.setCSSParser(cssParser)
        return cssParser

    def getCSSBuilder(self):
        return self.getCSSParser().getCSSBuilder()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getCSSDefaultMediumSet(klass):
        if klass.cssDefaultMediumSet is None:
            mediumSet = sets.Set()

            version = platform.python_version()
            mediumSet.add('-'.join(['python']).lower())
            mediumSet.add('-'.join(['python', version[:1]]).lower())
            mediumSet.add('-'.join(['python', version[:3]]).lower())
            mediumSet.add('-'.join(['python', version]).lower())

            system = [platform.system(), platform.release(), '.'.join(platform.version().split('.')[:2])]
            mediumSet.add('-'.join(['os'] + system[:1]).lower())
            mediumSet.add('-'.join(['os'] + system[:2]).lower())
            mediumSet.add('-'.join(['os'] + system[:3]).lower())

            mediumSet.add('-'.join(['os', sys.platform]).lower())

            klass.cssDefaultMediumSet = mediumSet
        return klass.cssDefaultMediumSet
    getCSSDefaultMediumSet = classmethod(getCSSDefaultMediumSet)
    def getCSSMediumSet(self):
        return self.getCSSBuilder().getMediumSet()
    def setCSSMediumSet(self, cssMediumSet):
        self.getCSSBuilder().setMediumSet(cssMediumSet)
    def updateCSSMediumSet(self, cssMediumSet):
        self.getCSSBuilder().updateMediumSet(cssMediumSet)
    cssMediumSet = property(getCSSMediumSet, setCSSMediumSet)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class XMLBuilderWithCSS(XMLBuilderCSSMixin, xmlBuilder.XMLBuilder):
    pass

