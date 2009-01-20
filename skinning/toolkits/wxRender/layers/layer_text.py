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

from _baseLayer import *
from TG.guiTools.pil.layers import TextLayer

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class layer_text(RenderLayerBase):
    def createWidget(self, parentObj):
        obj = TextLayer()
        self.layerOptions(obj)
        return obj

    def layerOptions(self, obj):
        text = self.getStyleSetting('text', 'TextLayer')
        obj.setText(text)

        pos = self.getStyleSettingEval('pos', None)
        if pos is not None:
            obj.setPosition(pos)

        size = self.getStyleSettingEval('size', None)
        if size is not None:
            obj.setSize(size)

        color = self.getStyleColorSetting('color', 'black').Get()
        obj.setColor(color)

        RenderLayerBase.layerOptions(self, obj)

