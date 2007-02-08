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
from TG.guiTools.pil.layers import GroupLayer

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class layer_group(LayerHandlerMixin, RenderLayerBase):
    def createWidget(self, parentObj):
        obj = GroupLayer()
        self.layerOptions(obj)
        return obj

    def addCollectedLayerChildElement(self, childElem, childObj):
        self.getObject().addLayer(childObj)

