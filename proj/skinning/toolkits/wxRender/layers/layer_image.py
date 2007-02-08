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
from TG.guiTools.pil.layers import ImageLayer

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class layer_image(RenderLayerBase):
    def createWidget(self, parentObj):
        ref = self.getStyleSettingRef()
        obj = self.openFrom(ref, False)
        return obj

    def finishWidget(self, obj, parentObj):
        if obj is None:
            ref = self.getStyleSettingRef()
            obj = self.openFrom(ref, False)
        return obj

    def openFrom(self, ref, setAsObject=True):
        if not ref: return None

        resource = self.getURIResolver().resolve(ref)
        imgRes = resource.open('rb')

        obj = ImageLayer.fromFile(imgRes)
        obj.setSourceRef(ref)
        self.layerOptions(obj)
        if setAsObject:
            self.setObject(obj)

        return obj

