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
from TG.guiTools.wx import listCtrl

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class list_item(wxPyWidgetBaseSkinElement):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    elementGlobals = wxPyWidgetBaseSkinElement.elementGlobals.copy()
    elementGlobals.update({
        'left': wx.LIST_FORMAT_LEFT,
        'right': wx.LIST_FORMAT_RIGHT,
        'center': wx.LIST_FORMAT_CENTER,
        })

    defaultSettings = wxPyWidgetBaseSkinElement.defaultSettings.copy()
    defaultSettings.update({ 
        })

    defaultStyleSettings = wxPyWidgetBaseSkinElement.defaultStyleSettings.copy()
    defaultStyleSettings.update({
        'align': 'LIST_FORMAT_LEFT',
        'col': '0',
        #'image': '-1',

        'index': 'None',
        #'width': '80',

        'text': 'A list item'

        #'font': ''
        #'fgcolor': ''
        #'bgcolor': ''
        })

    objParentTypes = wxClasses(wx.ListCtrl)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Definitions 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def createWidget(self, parentObj):
        obj = listCtrl.ListItem()
        self.initialListItemOptions(obj, parentObj)
        obj.addToList(parentObj, self.getStyleSettingEval('index'))
        return obj

    def finishWidget(self, obj, parentObj):
        pass

    def initialListItemOptions(self, obj, parentObj):
        stateMask = 0

        text = self.getStyleSettingLocalized('text')
        if text:
            obj.SetText(text)
            stateMask |= wx.LIST_MASK_TEXT

        column = self.getStyleSettingEval('col')
        obj.SetColumn(column)

        align = self.getStyleSettingEval('align')
        if align is not None:
            obj.SetAlign(align)
            stateMask |= wx.LIST_MASK_FORMAT

        width = self.getStyleSettingEval('width', None)
        if width is not None:
            obj.SetWidth(width)
            stateMask |= wx.LIST_MASK_WIDTH

        # image index
        imageIndex = self.getImageIndex('image', parentObj)
        if imageIndex is not None:
            obj.SetImage(imageIndex)
            stateMask |= wx.LIST_MASK_IMAGE

        # font and color
        font = self.getStyleFontSetting(None)
        if font:
            self.objSetFont(obj, font)
        fgColor = self.getStyleColorSetting('fgcolor', None)
        if fgColor is not None:
            obj.SetForegroundColour(fgColor)
        bgColor = self.getStyleColorSetting('bgcolor', None)
        if bgColor is not None:
            obj.SetBackgroundColour(bgColor)

        obj.SetMask(stateMask)
        return stateMask

    def getImageIndex(self, settingName, parentObj):
        imageIndex = self.getStyleSetting(settingName, None)
        if not imageIndex: 
            return None
        elif imageIndex.isdigit(): 
            return int(imageIndex)
        else:
            return parentObj.imageList.getIndexForPurpose(imageIndex)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def installDefaultEvent(self, evtHandler, evtObject, evtCallback):
        wx.EVT_LIST_ITEM_ACTIVATED(evtHandler, -1, evtCallback)

    def getEvtHostObject(self):
        return self.getObject()
    def getEvtObject(self):
        return None
    def getEvtHandler(self):
        obj = self.getObject()
        return obj.getItemEvtHandler(self.getParentObj())

