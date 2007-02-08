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

from PIL import ImageChops as _Chops

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Color Strategy
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class StrategyBase(object):
    def __repr__(self): 
        return self.getName()
    def getName(self):
        return self.__class__.__name__.lower()

    def combine(self, layer, imgLayer, imgBase):
        imgCombined = self._combine(imgLayer, imgBase)
        imgCombined = layer.callAlphaStrategy(imgCombined, imgLayer, imgBase) or imgCombined
        return imgCombined
    
    def combineAlpha(self, layer, imgCombined, imgLayer, imgBase):
        alphaCombined, alphaLayer, alphaBase = (imgCombined.split()[3], imgLayer.split()[3], imgBase.split()[3])
        alpha = self._combineAlpha(alphaCombined, alphaLayer, alphaBase)
        if alpha is not None:
            imgCombined.putalpha(alpha)
        return imgCombined
    
    def _combine(self, imgLayer, imgBase):
        return _Chops.composite(imgLayer, imgBase, imgLayer)

    def _combineAlpha(self, alphaCombined, alphaLayer, alphaBase):
        return _Chops.lighter(alphaLayer, alphaBase)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SourceLayer(StrategyBase):
    def getName(self):
        return "source"
    def combine(self, layer, imgLayer, imgBase):
        return imgLayer
    def combineAlpha(self, layer, imgCombined, imgLayer, imgBase):
        imgCombined.putalpha(imgLayer.split()[3])
        return imgCombined
layer = source = sourceLayer = SourceLayer()

class BaseLayer(StrategyBase):
    def getName(self): 
        return "base"
    def combine(self, layer, imgLayer, imgBase):
        return imgBase
    def combineAlpha(self, layer, imgCombined, imgLayer, imgBase):
        imgCombined.putalpha(imgBase.split()[3])
        return imgCombined
base = baseLayer = BaseLayer()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ PIL ImageChops blending stratigies
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ChopOpStrategy(StrategyBase):
    _chopop = staticmethod(lambda imgLayer, imgBase: imgLayer)
    alphaStrategy = None

    def __init__(self, *args, **kw):
        self.args, self.kw = args, kw

    def __repr__(self):
        args = ['%.5r'%i for i in self.args] + ['%s=%10r' % i for i in self.kw.iteritems()]
        args = ', '.join(args)
        if args:
            return '%s(%s)' % (self.getName(), args)
        else: 
            return self.getName()

    def __call__(klass, *args, **kw):
        return klass(*args, **kw)
    __call__ = classmethod(__call__)

    def _combine(self, imgLayer, imgBase):
        return self._chopop(imgLayer, imgBase, *self.args, **self.kw)

    def _combineAlpha(self, alphaCombined, alphaLayer, alphaBase):
        return self._combine(alphaLayer, alphaBase)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Composite(ChopOpStrategy):
    def _composite(self, layer, base):
        return _Chops.composite(layer, base, layer)
    _chopop = _composite
composite = Composite()

class Multiply(ChopOpStrategy):
    _chopop = staticmethod(_Chops.multiply)
    alphaStrategy = sourceLayer
multiply = Multiply()

class Lighter(ChopOpStrategy):
    _chopop = staticmethod(_Chops.lighter)
lighten = lighter = Lighter()
ChopOpStrategy.alphaStrategy = lighter

class Darker(ChopOpStrategy):
    _chopop = staticmethod(_Chops.darker)
darken = darker = Darker()

class Add(ChopOpStrategy):
    _chopop = staticmethod(_Chops.add)
add = Add()

class Subtract(ChopOpStrategy):
    _chopop = staticmethod(_Chops.subtract)
subtract = Subtract()

class Difference(ChopOpStrategy):
    _chopop = staticmethod(_Chops.difference)
difference = Difference()

class Invert(ChopOpStrategy):
    _chopop = staticmethod(_Chops.invert)
invert = Invert()

class Offset(ChopOpStrategy):
    _chopop = staticmethod(_Chops.offset)
offset = Offset(0.0, 0.0)

class Blend(ChopOpStrategy):
    _chopop = staticmethod(_Chops.blend)
    alphaStrategy = sourceLayer
blend = Blend(0.5)

class ColorDodge(Composite):
    alphaStrategy = sourceLayer
colordodge = colorDodge = ColorDodge()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Constants / Variables / Etc. 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

strategyMap = {
        "normal": composite,

        "layer": sourceLayer,
        "source": sourceLayer,
        "sourceLayer": sourceLayer,

        "base": baseLayer,
        "baseLayer": baseLayer,
        "dest": baseLayer,
        "destLayer": baseLayer,

        "mult": multiply,
        "multiply": multiply,

        "blend": blend,

        "add": add,
        "sub": subtract,
        "subtract": subtract,
        "diff": difference,
        "difference": difference,
        "invert": invert,
        "offset": offset,

        "min": darker,
        "darker": darken,
        "darken": darken,

        "max": lighter,
        "lighter": lighter,
        "lighten": lighter,

        "dodge": colordodge,
        "colordodge": colordodge,

        #"lineardodge": None,
        #"overlay": None,
        #"screen": None,

        #"colorburn": None,
        #"linearburn": None,
        #"dissolve": None,

        #"softlight": None,
        #"hardlight": None,
        #"vividlight": None,
        #"linearlight": None,
        #"penlight": None,
        #"hardmix": None,

        #"exclusion": None,
        #"hue": None,
        #"saturation": None,
        #"color": None,
        #"luminosity": None,
    }

