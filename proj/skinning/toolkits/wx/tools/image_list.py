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

from TG.skinning.toolkits.wx._baseElements import *
import image 

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SkinImageList(wx.ImageList):
    purposeMap = {}

    def Add(self, bitmap, mask=wx.NullBitmap, purposes=()):
        idx = wx.ImageList.Add(self, bitmap, mask)
        self.setImagePurposes(idx, purposes)
        return idx
    def AddWithColourMask(self, bitmap, colour, purposes=()):
        idx = wx.ImageList.AddWithColourMask(self, bitmap, colour)
        self.setImagePurposes(idx, purposes)
        return idx
    def AddIcon(self, icon, purposes=()):
        idx = wx.ImageList.AddIcon(self, icon)
        self.setImagePurposes(idx, purposes)
        return idx

    def getIndexForPurpose(self, purpose, default=NotImplemented):
        result = self.purposeMap.get(purpose, default)
        if result is NotImplemented:
            raise LookupError("Could not find image index for purpose \"%s\"" % purpose)
        return result

    def setImagePurposes(self, idx, purposes):
        if purposes and not self.purposeMap:
            self.purposeMap = self.purposeMap.copy()
        for purpose in purposes:
            self.purposeMap[purpose] = idx

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class image_list(image.BitmapImageHandlerMixin, wxPyWidgetBaseSkinElement):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    defaultSettings = wxPyWidgetBaseSkinElement.defaultSettings.copy()
    defaultSettings.update({ 
        })

    defaultStyleSettings = wxPyWidgetBaseSkinElement.defaultStyleSettings.copy()
    defaultStyleSettings.update({
        'size': '32,32',
        'mask': 'True',
        'count': '8',
        'for': '',
        })

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Definitions 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def createWidget(self, parentObj):
        kwWX = self.getStyleSettingsCollection(('size', 'mask', 'count'))
        kwWX.rename(initialCount='count')
        kwWX['width'], kwWX['height'] = kwWX.pop('size', (16,16))

        obj = SkinImageList(**kwWX)
        return obj

    def finishWidget(self, obj, parentObj):
        pass

    def addCollectedBitmapChild(self, childElem, childObj, purposes):
        imageIdx = self.getObject().Add(childObj, purposes=purposes)
        childElem.setSetting('image-idx-value', imageIdx)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getObjectPurposes(self):
        purposes = self.getStyleSetting('for').split(',')
        purposes = [purpose.strip() for purpose in purposes]
        return purposes

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ImageListHandlerMixin(object):
    _imageListTypes = wxClasses(wx.ImageList)

    def isChildCollector(self):
        return True
    def addCollectedChild(self, childElem, childObj): 
        if isinstance(childObj, self._imageListTypes):
            return self.addCollectedImageListChildElement(childElem, childObj, childElem.getObjectPurposes())
        return self.__super.addCollectedChild(childElem, childObj)

    def addCollectedImageListChildElement(self, childElem, imageList, purposes):
        raise NotImplementedError, 'Subclass responsibility'
ImageListHandlerMixin._ImageListHandlerMixin__super = super(ImageListHandlerMixin)

