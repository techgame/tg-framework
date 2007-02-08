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

import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
import blending

try: set
except NameError:
    from sets import Set as set

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class LayerBase(object):
    _blendStrategy = blending.composite
    _alphaStrategy = None
    _layerName = ""
    _renderPurposes = None
    defaultSize = (100, 100)
    defaultMode = "RGBA"
    strategyMap = blending.strategyMap

    def __init__(self, blend=None, alpha=None):
        if blend is not None:
            self.setBlendStrategy(blend)
        if alpha is not None:
            self.setAlphaStrategy(alpha)

    def save(self, filename, *args, **kw):
        self.getImage(*args, **kw).save(filename)
    def saveAlpha(self, filename):
        self.getImage(*args, **kw).split()[3].save(filename)

    #~ Printing and debug ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __repr__(self):
        return "%s(%s)" % (self.getLayerLabel(), ', '.join(self._reprArgs([])))

    def _reprArgs(self, args):
        args.append('blend=' + repr(self.getBlendStrategy()))
        args.append('alpha=' + repr(self.getAlphaStrategy()))
        return args

    def getLayerName(self):
        return self._layerName
    def setLayerName(self, layerName):
        if layerName:
            self._layerName = layerName

    def getLayerType(self):
        return self.__class__.__name__

    def getLayerLabel(self):
        name = self.getLayerName()
        if name:
            return '%s = %s' % (name, self.getLayerType())
        else: 
            return self.getLayerType()

    def _getDebugSaveName(self, *args):
        parts = args + (self.getLayerName(), self.getLayerType(), self.getBlendStrategy(), self.getAlphaStrategy())
        parts = '-'.join(map(str, parts))
        return parts

    def _debugSave(self, baseName='debug', level=()):
        name = self._getDebugSaveName(baseName, '.'.join(map(str, level)))
        img = self.getImage()
        if img:
            img.save(name + '.png')
            img.split()[3].save(name + '-alpha.png')

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Blending Strategies
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getMappedStrategy(klass, strategy):
        if isinstance(strategy, basestring):
            result = klass.strategyMap.get(strategy, None)
            if result is not None:
                return result
            elif ('(' in strategy) and (')' in strategy):
                name, args = strategy.split('(', 1)
                callableStrategy = klass.strategyMap.get(name, None)
                if callableStrategy is not None:
                    args = args[:args.index(')')].split(',')
                    args = map(float, args)
                    result = callableStrategy(*args)
                    return result
            raise ValueError("Unknown strategy directive %r" % (strategy,), strategy)

        return strategy

    getMappedStrategy = classmethod(getMappedStrategy)

    def getBlendStrategy(self):
        return self._blendStrategy
    def setBlendStrategy(self, blendStrategy):
        if blendStrategy:
            self._blendStrategy = self.getMappedStrategy(blendStrategy)
    blendStrategy = property(getBlendStrategy, setBlendStrategy)

    def callBlendStrategy(self, imgLayer, imgBase):
        blendStrategy = self.getBlendStrategy()
        blendStrategy = getattr(blendStrategy, 'combine', blendStrategy)
        return blendStrategy(self, imgLayer, imgBase)

    def getAlphaStrategy(self):
        return self._alphaStrategy or self.getBlendStrategy().alphaStrategy
    def setAlphaStrategy(self, alphaStrategy):
        if alphaStrategy:
            self._alphaStrategy = self.getMappedStrategy(alphaStrategy)
    alphaStrategy = property(getAlphaStrategy, setAlphaStrategy)

    def callAlphaStrategy(self, img, imgLayer, imgBase):
        alphaStrategy = self.getAlphaStrategy()
        alphaStrategy = getattr(alphaStrategy, 'combineAlpha', alphaStrategy)
        if alphaStrategy is None: 
            return img
        else: 
            return alphaStrategy(self, img, imgLayer, imgBase)

    def combine(self, nextImage, renderPurpose='', groupLayer=None):
        if nextImage is None:
            return self.getImage(renderPurpose, groupLayer)
        else:
            return self.callBlendStrategy(self.getImage(renderPurpose, groupLayer), nextImage)

    def getImage(self, renderPurpose=None, groupLayer=None):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    image = property(getImage)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Render sets technology
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def isEnabledFor(self, renderPurpose):
        if renderPurpose is None:
            return True

        myRenderFor = self.getRenderFor()
        if not myRenderFor:
            # default is membership in all renderPurposes
            return True 

        return (renderPurpose in myRenderFor)

    def getRenderFor(self):
        return self._renderPurposes
    def setRenderFor(self, renderPurposes):
        if isinstance(renderPurposes, basestring):
            renderPurposes = [s.strip() for s in renderPurposes.split(',')]
        self._renderPurposes = set(renderPurposes)
    def delRenderFor(self):
        # assure that it exists
        self._renderPurposes = None 
        del self._renderPurposes
    renderPurposes = property(getRenderFor, setRenderFor, delRenderFor)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Required layer methods
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getSize(self, allowDefault=True):
        return (allowDefault and self.defaultSize) or None
    def getMode(self, allowDefault=True):
        return (allowDefault and self.defaultMode) or None
    def isGroup(self):
        return False

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class GroupLayer(LayerBase):
    _layers = None

    def __init__(self, layers=(), *args, **kw):
        LayerBase.__init__(self, *args, **kw)
        self.extend(layers)

    def _debugPrint(self):
        from pprint import pprint
        pprint(self.iterTree(list))

    def iterTree(self, iterChild=iter):
        return self, iterChild(self.iterTreeChildren(iterChild))

    def iterTreeChildren(self, iterChild=iter):
        for each in self:
            if each.isGroup():
                yield each, iterChild(each.iterTreeChildren(iterChild))
            else:
                yield each,

    def _debugSave(self, baseName='debug', level=[]):
        level = level[:] + [0]
        for idx, layer in enumerate(self.getLayers()):
            level[-1] = idx
            layer._debugSave(baseName, level)
        LayerBase._debugSave(self, baseName, level[:-1])

    def __iter__(self):
        return iter(self.getLayers())

    def __len__(self):
        return len(self.getLayers())
    def __getitem__(self, idx):
        return self.getLayers().__len__(idx)
    def __setitem__(self, idx, value):
        return self.getLayers().__setitem__(idx, value)
    def __delitem__(self, idx):
        return self.getLayers().__delitem__(idx)

    def getLayers(self):
        if self._layers is None:
            self.setLayers([])
        return self._layers
    def setLayers(self, layers):
        self._layers = list(layers)
    layers = property(getLayers, setLayers)

    def addLayer(self, layer):
        if not isinstance(layer, LayerBase):
            layer = GroupLayer(layer)
        self.getLayers().append(layer)
    add = append = addLayer
    def removeLayer(self, layer):
        self.getLayers().remove(layer)
    remove = removeLayer

    def extendLayers(self, layers):
        for l in layers:
            self.addLayer(l)
    extend = extendLayers

    def getImage(self, renderPurpose=None, groupLayer=None):
        if not self.isEnabledFor(renderPurpose):
            return None

        img = None
        for layer in self.getLayers()[::-1]:
            if layer.isEnabledFor(renderPurpose):
                img = layer.combine(img, renderPurpose, self)
        return img

    def getMode(self, allowDefault=True):
        for layer in self.getLayers():
            mode = layer.getMode()
            if mode is not None:
                return mode
        return LayerBase.getMode(self, allowDefault)
    def getSize(self, allowDefault=True):
        for layer in self.getLayers():
            size = layer.getSize()
            if size is not None:
                return size
        return LayerBase.getSize(self, allowDefault)

    def isGroup(self):
        return True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ImageLayer(LayerBase):
    _image = None
    _sourceRef = None

    def __init__(self, image=None, *args, **kw):
        LayerBase.__init__(self, *args, **kw)
        if image is not None:
            self.setImage(image)

    def _reprArgs(self, args):
        args.append('source=' + repr(self.getSourceRef()))
        return LayerBase._reprArgs(self, args)

    def getSourceRef(self):
        return self._sourceRef or getattr(self.getImage(), 'filename', None) or '<unknown>'
    def setSourceRef(self, sourceRef):
        self._sourceRef = sourceRef
    sourceRef = property(getSourceRef, setSourceRef)

    def getImage(self, renderPurpose=None, groupLayer=None):
        if not self.isEnabledFor(renderPurpose):
            return None
        return self._image
    def setImage(self, image):
        if image is None:
            raise ValueError('Must set a valid image instance, not None')
        self._image = image
    image = property(getImage, setImage)

    def setImageFromFile(self, imageFile):
        img = Image.open(imageFile)
        self.setImage(img)
        return img

    def getMode(self, allowDefault=True):
        return self.getImage().mode or LayerBase.getMode(self, allowDefault)
    def getSize(self, allowDefault=True):
        return self.getImage().size or LayerBase.getSize(self, allowDefault)

    def fromColor(klass, color, size, mode=None, *args, **kw):
        if mode is None:
            mode = {1:'L', 3:'RGB', 4:'RGBA'}[len(color)]
        image = PIL.Image.new(mode, size, color)
        return klass(image, *args, **kw)
    fromColor = classmethod(fromColor)
    
    def fromFile(klass, file, *args, **kw):
        image = PIL.Image.open(file)
        return klass(image, *args, **kw)
    fromFile = classmethod(fromFile)

    def fromImage(klass, image, *args, **kw):
        return klass(image, *args, **kw)
    fromImage = classmethod(fromImage)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ColorLayer(LayerBase):
    _color = None
    _mode = None
    _size = None
    _cache = None

    def __init__(self, color=None, size=None, mode=None, *args, **kw):
        LayerBase.__init__(self, *args, **kw)
        if color is not None: self.setColor(color)
        if size is not None: self.setSize(size)
        if mode is not None: self.setMode(mode)

    def getColor(self):
        return self._color
    def setColor(self, color):
        self._color = color
    color = property(getColor, setColor)

    def getSize(self, allowDefault=True, defaultLayer=None):
        return self._size or (defaultLayer and defaultLayer.getSize()) or LayerBase.getSize(self, allowDefault)
    def setSize(self, size):
        self._size = size
    size = property(getSize, setSize)

    def getMode(self, allowDefault=True, defaultLayer=None):
        return self._mode or (defaultLayer and defaultLayer.getMode()) or LayerBase.getMode(self, allowDefault)
    def setMode(self, mode):
        self._mode = mode
    mode = property(getMode, setMode)

    def getImage(self, renderPurpose=None, groupLayer=None):
        if not self.isEnabledFor(renderPurpose):
            return None
        if self._cache is None:
            self._cache = {}

        size = self.getSize(True, groupLayer)

        img = self._cache.get(size)
        if img is None:
            img = PIL.Image.new(self.getMode(True, groupLayer), size, self.getColor())
            self._cache[size] = img
        return img

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TextLayer(LayerBase):
    def __init__(self, text='Text Layer', color=None, size=None, mode=None, *args, **kw):
        LayerBase.__init__(self, *args, **kw)
        if text is not None: self.setText(text)
        if color is not None: self.setColor(color)
        if size is not None: self.setSize(size)
        if mode is not None: self.setMode(mode)

    _text = "Text Layer"
    def getText(self):
        return self._text
    def setText(self, text):
        self._text = text
    text = property(getText, setText)

    _color = None
    def getColor(self):
        return self._color
    def setColor(self, color):
        self._color = color
    color = property(getColor, setColor)

    _position = (0,0)
    def getPosition(self):
        return self._position
    def setPosition(self, position):
        self._position = position
    position = property(getPosition, setPosition)

    _size = None
    def getSize(self, allowDefault=True, defaultLayer=None):
        return self._size or (defaultLayer and defaultLayer.getSize()) or LayerBase.getSize(self, allowDefault)
    def setSize(self, size):
        self._size = size
    size = property(getSize, setSize)

    _mode = None
    def getMode(self, allowDefault=True, defaultLayer=None):
        return self._mode or (defaultLayer and defaultLayer.getMode()) or LayerBase.getMode(self, allowDefault)
    def setMode(self, mode):
        self._mode = mode
    mode = property(getMode, setMode)

    _font = PIL.ImageFont.truetype('/Library/Fonts/Chalkboard.ttf', 24, index=0, encoding='ascii')
    def getFont(self):
        return self._font
    def setFont(self, font):
        self._font = font
    font = property(getFont, setFont)

    def getImage(self, renderPurpose=None, groupLayer=None):
        if not self.isEnabledFor(renderPurpose):
            return None

        size = self.getSize(True, groupLayer)
        mode = self.getMode(True, groupLayer)
        color = self.getColor()

        img = PIL.Image.new(mode, size, (0xff,0,0,0))
        imgDraw = PIL.ImageDraw.ImageDraw(img)
        imgDraw.text(self.getPosition(), unicode(self.getText()), self.getColor(), font=self.getFont())
        return img

