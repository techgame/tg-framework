##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##~ Copyright (C) 2002-2004  TechGame Networks, LLC.
##~ 
##~ This library is free software; you can redistribute it and/or
##~ modify it under the terms of the BSD style License as found in the 
##~ LICENSE file included with this distribution.
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""Translate from CSS2 style font specifications into wxPython compatible fonts.

Intended for use with TG.w3c.cssParser parsed entities.

Using http://www.w3.org/TR/CSS21/fonts.html as rough reference document.
"""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import wx
from __init__ import wxVersion, wxClasses

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

_FontBase = wxClasses(wx.Font)[0]
if not hasattr(_FontBase, 'GetLineHeight'):
    def GetLineHeight(self):
        sdc = wx.ScreenDC()
        return sdc.GetFullTextExtent('Wy', self)[1]

    _FontBase.GetLineHeight = GetLineHeight

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CSSFont(wx.Font):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    _genericFamilyTable = {
        None: wx.DEFAULT,
        'serif': wx.ROMAN,
        'sans-serif': wx.SWISS,
        'cursive': wx.SCRIPT,
        'fantasy': wx.DECORATIVE,
        'monospace': wx.MODERN,
        }

    _styleTable = {
        #"normal": wx.NORMAL,
        #"italic": wx.ITALIC,
        #"oblique": wx.SLANT,
        'normal': wx.FONTFLAG_DEFAULT,
        'italic': wx.FONTFLAG_ITALIC,
        'slant': wx.FONTFLAG_SLANT,
        'oblique': wx.FONTFLAG_SLANT,

        'light': wx.FONTFLAG_LIGHT,
        'bold': wx.FONTFLAG_BOLD,
        #'': wx.FONTFLAG_ANTIALIASED,
        #'': wx.FONTFLAG_NOT_ANTIALIASED,
        'underline': wx.FONTFLAG_UNDERLINED,
        'strike': wx.FONTFLAG_STRIKETHROUGH,
        'strikethrough': wx.FONTFLAG_STRIKETHROUGH,

        wx.NORMAL: wx.FONTFLAG_DEFAULT, 
        wx.SLANT: wx.FONTFLAG_SLANT,
        wx.ITALIC: wx.FONTFLAG_ITALIC,
        wx.LIGHT: wx.FONTFLAG_LIGHT,
        wx.BOLD: wx.FONTFLAG_BOLD,
        }

    _variantTable = {
        "normal": None,
        "small-caps": None,
        }

    _weightTable = {
        "light": 300,
        "lighter": 300, # fake relativness for now
        "normal": 400,
        "bold": 700,
        "bolder": 700, # fake relativness for now

        "100": 100,
        "200": 200,
        "300": 300,
        "400": 400,
        "500": 500,
        "600": 600,
        "700": 700,
        "800": 800,
        "900": 900,

        wx.LIGHT: 300,
        wx.NORMAL: 400,
        wx.BOLD: 700,

        wx.FONTFLAG_LIGHT: 300,
        wx.FONTFLAG_BOLD: 700,
        } 

    _absSizeTable = {
        "xx-small" : 3./5.,
        "x-small": 3./4.,
        "small": 8./9.,
        "medium": 1./1.,
        "normal": 1./1.,
        "large": 6./5.,
        "x-large": 3./2.,
        "xx-large": 2./1.,
        "xxx-large": 3./1.,
        }

    _relSizeTable = {
        'pt': 
            # pt: absolute point size
            # Note: this is 1/72th of an inch
            (lambda value, pt: value),
        'px':
            # px: pixels, relative to the viewing device
            # Note: approximate at the size of a pt
            (lambda value, pt: value),
        'ex':
            # ex: proportional to the 'x-height' of the parent font
            # Note: can't seem to dervie this value from wx.Font methods,
            # so we'll approximate by calling it 1/2 a pt
            (lambda value, pt: 2 * value),
        'pc':
            # pc: 12:1 pica:point size
            # Note: this is 1/6th of an inch
            (lambda value, pt: 12*value),
        'in':
            # in: 72 inches per point
            (lambda value, pt: 72*value),
        'cm':
            # in: 72 inches per point, 2.54 cm per inch
            (lambda value, pt,_r=72./2.54: _r*value),
        'mm':
            # in: 72 inches per point, 25.4 mm per inch
            (lambda value, pt,_r=72./25.4: _r*value),
        '%':
            # %: percentage of the parent's pointSize
            (lambda value, pt: 0.01 * pt * value),
        'em':
            # em: proportional to the 'font-size' of the parent font
            (lambda value, pt: pt * value),
        }

    defaultFont = None

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Factory Methods
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def fromCSSFont(klass, fontValues, parentFont=None):
        parentFont = parentFont or klass.getDefaultFont()
        kw = klass._getDefaultArgs(parentFont)
        kw.update(klass.cssFont(fontValues, parentFont))
        return klass(**kw)
    fromCSSFont = classmethod(fromCSSFont)

    def fromCSS(klass, cssValueDict, parentFont=None):
        parentFont = parentFont or klass.getDefaultFont()
        kw = klass._getDefaultArgs(parentFont)
        cssValue = cssValueDict.get('font')
        if cssValue: 
            kw.update(klass.cssFont(cssValue, parentFont))
        cssValue = cssValueDict.get('font-family')
        if cssValue: 
            kw.update(klass.cssFamilies(cssValue, parentFont))
        cssValue = cssValueDict.get('font-style')
        if cssValue: 
            kw.update(klass.cssStyle(cssValue, parentFont))
        cssValue = cssValueDict.get('font-variant')
        if cssValue: 
            kw.update(klass.cssVariant(cssValue, parentFont))
        cssValue = cssValueDict.get('font-weight')
        if cssValue: 
            kw.update(klass.cssWeight(cssValue, parentFont))
        cssValue = cssValueDict.get('font-size')
        if cssValue: 
            kw.update(klass.cssSize(cssValue, parentFont))
        cssValue = cssValueDict.get('line-height')
        if cssValue: 
            kw.update(klass.cssLineHeight(cssValue, parentFont))

        kw['flags'] = kw.pop('style', 0) | kw.pop('weight', 0)
        font = wx.FFont(**kw)
        font.__class__ = klass
        return font
    fromCSS = classmethod(fromCSS)

    def _getDefaultArgs(klass, parentFont):
        parentFont = parentFont or klass.getDefaultFont()
        return klass._attrResult(
                font_size=parentFont.GetPointSize(),
                font_family=parentFont.GetFamily(), 
                font_style=klass._styleTable[parentFont.GetStyle()],
                font_weight=klass._styleTable[parentFont.GetWeight()])
    _getDefaultArgs = classmethod(_getDefaultArgs)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public Class Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getDefaultFont(klass):
        if klass.defaultFont is None:
            klass.defaultFont = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)
            klass.defaultPointSize = klass.defaultFont.GetPointSize()
        return klass.defaultFont
    getDefaultFont = classmethod(getDefaultFont)

    def getFacenameTable(klass):
        if klass._facenameTable is None:
            enumerator = wx.FontEnumerator()
            enumerator.EnumerateFacenames()
            klass._facenameTable = {}
            for name in enumerator.GetFacenames():
                klass._facenameTable[name.lower()] = name
        return klass._facenameTable
    getFacenameTable = classmethod(getFacenameTable)
    _facenameTable = None

    def cssFamilies(klass, families, parentFont=None):
        """Determines family and/or face name.

        We're treating "specific" family names as wx font facenames
        For generic family names, translate them into the wx constants: 
            [wx.DEFAULT, wx.DECORATIVE, wx.ROMAN, wx.SCRIPT, wx.SWISS, wx.MODERN]
        """
        parentFont = parentFont or klass.getDefaultFont()

        facenameTable = klass.getFacenameTable()
        genericFamilyTable = klass._genericFamilyTable
        for family in families:
            family = family.lower()

            result = facenameTable.get(family)
            if result is not None: 
                return klass._attrResult(font_face=result)

            result = genericFamilyTable.get(family)
            if result is not None: 
                return klass._attrResult(font_family=result)

        return klass._attrResult(font_family=wx.DEFAULT)
    cssFamilies = classmethod(cssFamilies)

    def cssStyle(klass, style, parentFont=None):
        """Determines italic or "normal" style.
        
        normal | italic | oblique | inherit"""
        parentFont = parentFont or klass.getDefaultFont()
        style = style.strip().lower()
        #result = klass._styleTable.get(style, wx.NORMAL)
        result = klass._styleTable.get(style, klass._styleTable['normal'])
        return klass._attrResult(font_style=result)
    cssStyle = classmethod(cssStyle)

    def cssVariant(klass, variant, parentFont=None):
        """Not used for wx.Font, but presented because of CSS support
        
        normal | small-caps | inherit
        """
        parentFont = parentFont or klass.getDefaultFont()
        result = variant.lower()
        return klass._attrResult(font_variant=result)
    cssVariant = classmethod(cssVariant)

    def cssWeight(klass, weight, parentFont=None):
        """Provides normal, light or bold emphasis for the wx.Font weight attribute.
        
        normal | bold | bolder | lighter | 100 | 200 | 300 | 400 | 500 | 600 | 700 | 800 | 900 | inherit

        Note: bolder and lighter are aliased to wx.BOLD and wx.LIGHT for now. 
        """
        parentFont = parentFont or klass.getDefaultFont()

        weight = weight.strip().lower()
        if weight.isdigit():
            weightValue = int(weight)
        else:
            weightValue = klass._weightTable.get(weight, 400)

        if weightValue <= 300: 
            result = wx.FONTFLAG_LIGHT #wx.LIGHT
        elif 700 <= weightValue: 
            result = wx.FONTFLAG_BOLD #wx.BOLD
        else:
            result = wx.FONTFLAG_DEFAULT #wx.NORMAL
        return klass._attrResult(font_weight=result)
    cssWeight = classmethod(cssWeight)

    def cssSize(klass, size, parentFont=None):
        """Provides the point size from CSS description of size
        
        <absolute-size> | <relative-size> | <length> | <percentage> | inherit"""
        parentFont = parentFont or klass.getDefaultFont()
        parentSize = parentFont.GetPointSize()

        if size in klass._absSizeTable:
            result = klass.defaultPointSize * klass._absSizeTable[size]
        elif isinstance(size, tuple):
            value, unit = float(size[0]), size[1].lower()
            result = klass._relSizeTable[unit](value, parentSize)
        elif size == 'larger':
            larger = [parentSize*x for x in klass._absSizeTable.values() if parentSize*x > parentSize+1]
            larger.sort()
            result = larger and larger[0] or parentSize
        elif size == 'smaller':
            smaller = [parentSize*x for x in klass._absSizeTable.values() if parentSize*x < parentSize-1]
            smaller.sort()
            result = (smaller and smaller[-1]) or parentSize
        else:
            result = float(size)

        return klass._attrResult(font_size=result)
    cssSize = classmethod(cssSize)

    def cssLineHeight(klass, lineheight, parentFont=None):
        """Not used for wx.Font, but presented because of CSS support"""
        parentFont = parentFont or klass.getDefaultFont()

        parentLineHeight = parentFont.GetLineHeight()

        if lineheight in klass._absSizeTable:
            result = klass.defaultPointSize * klass._absSizeTable[lineheight]
        elif isinstance(lineheight, tuple):
            value, unit = float(lineheight[0]), lineheight[1].lower()
            result = klass._relSizeTable[unit](value, parentLineHeight)
        elif lineheight == 'larger':
            larger = [parentLineHeight*x for x in klass._absSizeTable.values() if parentLineHeight*x > parentLineHeight+1]
            larger.sort()
            result = larger and larger[0] or parentLineHeight
        elif lineheight == 'smaller':
            smaller = [parentLineHeight*x for x in klass._absSizeTable.values() if parentLineHeight*x < parentLineHeight-1]
            smaller.sort()
            result = (smaller and smaller[-1]) or parentLineHeight
        else:
            result = float(lineheight)

        return klass._attrResult(line_height=result)
    cssLineHeight = classmethod(cssLineHeight)


    def cssFont(klass, fontValues, parentFont=None):
        """	[ [ <'font-style'> || <'font-variant'> || <'font-weight'> ]? <'font-size'> [ / <'line-height'> ]? <'font-family'> ] | inherit"""
        parentFont = parentFont or klass.getDefaultFont()

        result = {}
        fontParts = list(fontValues)
        part = fontParts.pop(0)

        while fontParts:
            if part in klass._styleTable:
                result.update(klass.cssStyle(part, parentFont))
                part = fontParts.pop(0)
            elif part in klass._variantTable:
                result.update(klass.cssVariant(part, parentFont))
                part = fontParts.pop(0)
            elif part in klass._weightTable:
                result.update(klass.cssWeight(part, parentFont))
                part = fontParts.pop(0)
            else:
                break

        if isinstance(part, tuple) and len(part) == 3:
            fontSize, slash, lineHeight = part
            assert slash == '/'
            result.update(klass.cssSize(fontSize, parentFont))
            result.update(klass.cssLineHeight(lineHeight, parentFont))
        else:
            result.update(klass.cssSize(part, parentFont))

        result.update(klass.cssFamilies(fontParts))
        return result
    cssFont = classmethod(cssFont)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __repr__(self):
        return '<%s "%s">' % (self.__class__.__name__, self.GetNativeFontInfoDesc())


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Protected Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    _attrNameMap = {
        'font_face': ('face', None),
        'font_family': ('family', None),
        'font_style': ('style', None),
        'font_size': ('pointSize', int),
        'font_weight': ('weight', int)
        #'line-height': ('size', int),
        #'font-variant': (None, None),
        }

    #if wxVersion() < '2.5':
    #    _attrNameMap['font-face'] = ('faceName', None) # in 2.4 "face" was called "faceName"

    def _attrResult(klass, **kw):
        """Convert css-style names to wx.Font like names, including any necessary conversions"""
        result = {}
        for name, value in kw.items():
            newName, xform = klass._attrNameMap.get(name, (None, None))
            if not newName:
                continue
            if xform:
                value = xform(value)
            result[newName] = value
        return result
    _attrResult = classmethod(_attrResult)

