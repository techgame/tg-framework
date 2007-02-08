##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~ Copyright (C) 2002-2005  TechGame Networks, LLC.              ##
##~                                                               ##
##~ This library is free software; you can redistribute it        ##
##~ and/or modify it under the terms of the BSD style License as  ##
##~ found in the LICENSE file included with this distribution.    ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from TG.skinning.toolkits.wxRender._baseElements import wxPyWidgetBaseSkinElement
from TG.guiTools.pil import layers

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class RenderLayerMixin(object):
    def layerOptions(self, obj):
        name = self.getStyleSetting('name', None)
        if name is not None:
            obj.setLayerName(name)

        forPurpose = self.getStyleSetting('for', None)
        if forPurpose is not None:
            obj.setRenderFor(forPurpose)

        blend = self.getStyleSetting('blend', '')
        if blend:
            obj.setBlendStrategy(blend)
        alpha = self.getStyleSetting('alpha', '')
        if alpha:
            obj.setAlphaStrategy(alpha)

class LayerHandlerMixin(object):
    def isChildCollector(self):
        return True
    def addCollectedChild(self, childElem, childObj): 
        if isinstance(childElem, RenderLayerBase):
            if childObj is not None:
                return self.addCollectedLayerChildElement(childElem, childObj)
            else: return False
        return self.__super.addCollectedChild(childElem, childObj)

    def addCollectedLayerChildElement(self, childElem, childObj):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
LayerHandlerMixin._LayerHandlerMixin__super = super(LayerHandlerMixin)

class RenderLayerBase(RenderLayerMixin, wxPyWidgetBaseSkinElement):
    def addCollectedLayerChildElement(self, childElem, childObj):
        obj = self.getObject().addLayerAndReplace(childObj)
        if obj is not None:
            self.setObject(obj)

