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

import css
import element

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ CSS Skin Context
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SkinContextCSSMixin(object):
    CSSCascadeFactory = css.CSSCascadeStrategy
    def getCSSCascade(self):
        try:
            return self.cssCascade
        except AttributeError:
            return self.createCSSCascade()
    def setCSSCascade(self, cssCascade):
        self.cssCascade = cssCascade

    def createCSSCascade(self):
        cascade = self.CSSCascadeFactory()
        cascade.setParser(self.getSkinner().getCSSParser())
        self.setCSSCascade(cascade)
        return cascade

    def updateCSSCascade(self, author=None, user=None, userAgent=None):
        self.getCSSCascade().merge(author, user, userAgent)

    def onNewSkinElement(self, skinElement):
        self.setCSSCascade(self.getCSSCascade().copy())

class CSSSkinContext(SkinContextCSSMixin, element.SkinContext):
    pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ CSS Skin Element
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SkinElementCSSMixin(object):
    defaultStyleSettings = {}
    SkinContextFactory = CSSSkinContext
    CSSElementInterfaceFactory = css.CSSSkinElementInterface
    _cssElement = None
    _cssCascade = None
    _cssUsedValues = {}

    def isCSSEnabled(self):
        return True

    def getCSSElement(self): 
        return self._cssElement
    def setCSSElement(self, cssElement): 
        self._cssElement = cssElement
    def setupCSSElement(self, elemBuilder, node, attributes, namespaceMap):
        cssElem = self.CSSElementInterfaceFactory(self, node, attributes, namespaceMap)
        self.setCSSElement(cssElem)

    def getCSSElementFrom(self, other): 
        if other is not None:
            try: 
                return other.getCSSElement()
            except AttributeError: 
                pass
        return None
    def addCSSElement(self, element, srcref):
        elem = self.getCSSElementFrom(element)
        if elem is not None:
            self.getCSSElement().addElement(elem, srcref)

    def getCSSCascade(self):
        if self._cssCascade is None:
            self.setCSSCascade(self.getContext().getCSSCascade())
        return self._cssCascade
    def setCSSCascade(self, cascade):
        if cascade is None:
            self.delCSSCascade()
        else:
            self._cssCascade = cascade
    def delCSSCascade(self):
        if self._cssCascade is not None:
            del self._cssCascade

    def getCSSParser(self):
        cascade = self.getCSSCascade()
        if cascade:
            return cascade.getParser()

    def hasStyleSetting(self, *names, **kw):
        nonDefault = kw.pop('nonDefault', False)
        uniqueObject = kw
        for name in names:
            style, how = self.getStyleSettingEx(name, uniqueObject , **kw)
            if style is uniqueObject:
                continue # not found
            if nonDefault and how == 'default':
                continue # found a default

            # looks like we have a valid setting...
            return True 
        # hum... nothing found, or nothing searched for
        return False

    def getStyleSetting(self, name, default=NotImplemented, **kw):
        return self.getStyleSettingEx(name, default, **kw)[0]
    def getStyleSettingEx(self, name, default=NotImplemented, **kw):
        if name in self._cssUsedValues:
            return self._cssUsedValues[name]

        style, how = self.getComputedStyleSettingEx(name, NotImplemented, **kw)
        if style is NotImplemented:
            # use default
            style, how = self.defaultStyleSettings.get(name, default), 'default'
            if style is NotImplemented: 
                raise LookupError("Could not find a style setting for \'%s\'" % (name,))

        if not self._cssUsedValues:
            self._cssUsedValues = {}
        self._cssUsedValues[name] = (style, how)

        return (style, how)

    def getStyleSettingRef(self, default=''):
        return self.getStyleSetting('ref', None) or self.getStyleSetting('href', default)

    def getStyleSettingInContext(self, name, default=NotImplemented):
        value = self.getStyleSetting(name, None)
        return self._getSettingInContextImpl(value, name, default)

    def getComputedStyleSetting(self, name, default=NotImplemented, **kw):
        return self.getComputedStyleSettingEx(name, default, **kw)[0]
    def getComputedStyleSettingEx(self, name, default=NotImplemented, **kw):
        style, how = self.getSpecifiedStyleSettingEx(name, default, **kw)
        if style == 'inherit':
            style, how = default, 'default'
            for xmlParent in self.iterXMLParents():
                if xmlParent.hasStyleSetting(name):
                    style, how = xmlParent.getStyleSetting(name, **kw), 'inherit'
                    break

        if style == 'default':
            result = self.defaultStyleSettings.get(name, NotImplemented)
            if result is not None:
                style, how = result, 'specified-default'

        return (style, how)

    def getSpecifiedStyleSetting(self, name, default=NotImplemented, **kw):
        return self.getSpecifiedStyleSettingEx(name, default, **kw)[0]
    def getSpecifiedStyleSettingEx(self, name, default=NotImplemented, forceCSS=False):
        if self.hasSetting(name):
            style, how = self.getSetting(name), 'specified'
            if forceCSS:
                style = self.getCSSParser().parseSingleAttr(style)
        else:
            result = self.getCSSCascade().findStyleFor(self.getCSSElement(), name, None)
            if result is not None:
                style, how = result, 'css'
            else: 
                style, how = default, 'default'

        return (style, how)

    def iterAllCSS(self, bSorted=False):
        return self.getCSSCascade().findAllCSSRulesFor(self.getCSSElement(), bSorted)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Debug
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def debugCSS(self, bPrint=True, leader=''):
        result = list(self.iterAllCSS(bSorted=True))
        if bPrint:
            for e in result:
                print '%s%r' % (leader, e)
        return result

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ CSSSkinElement mixed together
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CSSSkinElement(SkinElementCSSMixin, element.SkinElement):
    pass

