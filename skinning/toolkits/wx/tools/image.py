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

import os
import warnings
import mimetypes

try: 
    from cStringIO import StringIO
except ImportError: 
    from StringIO import StringIO

from TG.skinning.toolkits.wx._baseElements import *

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ImageSkinElementBase(object):
    def getObjectPurposes(self):
        purposes = self.getStyleSetting('for').split(',')
        purposes = [purpose.strip() for purpose in purposes]
        return purposes

    def getObjectAsImage(self):
        obj = self.getObject()
        if obj and obj.Ok():
            return self.getObject()
    def getObjectAsBitmap(self):
        obj = self.getObject()
        if obj and obj.Ok():
            return self.getObject().ConvertToBitmap()
    def getObjectAsIcon(self):
        bmp = self.getObjectAsBitmap()
        if bmp and bmp.Ok():
            return wx.IconFromBitmap(bmp)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class image(ImageSkinElementBase, wxPyWidgetBaseSkinElement):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    defaultSettings = wxPyWidgetBaseSkinElement.defaultSettings.copy()
    defaultSettings.update({ 
        })

    defaultStyleSettings = wxPyWidgetBaseSkinElement.defaultStyleSettings.copy()
    defaultStyleSettings.update({
        #'ref': '',
        'type': '',
        'index': '-1',
        'for': '',
        })

    objParentTypes = ()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Definitions 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def createWidget(self, parentObj):
        ref = self.getStyleSettingRef()
        if ref:
            return self.openFrom(ref, False)
        else:
            return None

    def finishWidget(self, obj, parentObj):
        if obj is None:
            ref = self.getStyleSettingRef()
            if ref:
                return self.openFrom(ref, False)
        else:
            return None

    def resolveFile(self, ref=None):
        ref, index = self.getRefAndIndex(ref)
        return self.getURIResolver().resolve(ref).open('rb')

    def asPILImage(self, ref=None):
        from PIL import Image
        return Image.open(self.resolveFile(ref))

    def getRefAndIndex(self, ref=None):
        ref = ref or self.getStyleSettingRef()
        refEx = ref.split('#', 1) + [0]
        return refEx[0], int(refEx[1])

    def openFrom(self, ref, doSetObject=True):
        mimeType = self.getStyleSetting('type')
        ref, index = self.getRefAndIndex(ref)
        if not mimeType:
            mimeType = mimetypes.guess_type(ref, strict=False)[0]

        obj = self._imageFromStream(self.resolveFile(ref), index, mimeType)

        if doSetObject:
            self.setObject(obj)
        return obj

    def _imageFromStream(self, imageFile, index, mimeType, imageType=wx.BITMAP_TYPE_ANY):
        if mimeType:
            return wx.ImageFromStreamMime(imageFile, mimeType, index)
        else:
            return wx.ImageFromStream(imageFile, imageType, index)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Image Handler Mixin
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ImageHandlerMixin(object):
    def isChildCollector(self):
        return True
    def addCollectedChild(self, childElem, childObj): 
        if isinstance(childElem, ImageSkinElementBase):
            if childObj is not None:
                return self.addCollectedImageChildElement(childElem, childObj)
            else: return False
        return self.__super.addCollectedChild(childElem, childObj)

    def addCollectedImageChildElement(self, childElem, childObj):
        return self.addCollectedImageChild(childElem, childObj, childElem.getObjectPurposes())

    def addCollectedImageChild(self, childElem, image, purposes):
        raise NotImplementedError, 'Subclass responsibility'
ImageHandlerMixin._ImageHandlerMixin__super = super(ImageHandlerMixin)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class BitmapImageHandlerMixin(ImageHandlerMixin):
    def addCollectedImageChild(self, childElem, image, purposes):
        bitmap = childElem.getObjectAsBitmap()
        if bitmap:
            return self.addCollectedBitmapChild(childElem, bitmap, purposes)

    def addCollectedBitmapChild(self, childElem, bitmap, purposes):
        raise NotImplementedError, 'Subclass responsibility'

    def _setSizeFromBitmap(self, obj, bitmap):
        sizeImgOpt = self.getStyleSetting('size-img', 'inherit').lower()
        if (sizeImgOpt == 'inherit'):
            # update the size for the control
            w,h = obj.GetSize()
            w,h = max(w, bitmap.GetWidth()), max(h, bitmap.GetHeight())
            obj.SetSize((w,h))
        elif (sizeImgOpt in ('none', '')):
            pass

