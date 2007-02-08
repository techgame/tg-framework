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

from TG.guiTools.wx.subjectEvtHandler import SubjectEvtHandler
from TG.skinning.engine.xmlSkinner import XMLFactory
from TG.skinning.toolkits.wx._baseElements import *

from menu import MenuCommon

import image

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class menu_item(image.BitmapImageHandlerMixin, MenuCommon):
    defaultSettings = MenuCommon.defaultSettings.copy()
    defaultSettings.update({ 
        'wxid':'NewId()',
        })

    defaultStyleSettings = MenuCommon.defaultStyleSettings.copy()
    defaultStyleSettings.update({
        'text': 'Menu Item',
        'help': '',
        'checkable': '0',
        'checked': 'None',
        })

    objParentTypes = wxClasses(wx.Menu)
    menubarParentType = wxClasses(wx.MenuBar)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Definitions 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def createWidget(self, parentObj):
        text = self.getStyleSettingLocalized('text')
        text = text.replace('\\t', '\t')
        text = text.replace('|', '\t').replace('\t\t', '|')
        checked = self.getStyleSettingEval('checked')
        checkable = checked is not None or self.getStyleSettingEval('checkable')
        kind = 0
        if checkable:
            kind |= wx.ITEM_CHECK

        obj = wx.MenuItem(parentObj, 
            self.getSettingEval('wxid'), 
            text,
            self.getStyleSettingLocalized('help'), 
            kind)
        return obj

    def finishWidget(self, obj, parentObj):
        parentObj.AppendItem(obj)
        checked = self.getStyleSettingEval('checked')
        if checked is not None:
            obj.Check(checked)

    def installDefaultEvent(self, evtHandler, evtObject, evtCallback):
        wx.EVT_MENU(evtHandler, evtObject.GetId(), evtCallback)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def addCollectedBitmapChild(self, childElem, bitmap, purposes):
        obj = self.getObject()
        try: 
            # Some platforms don't have "SetBitmaps" on their menus
            obj.SetBitmaps 
        except AttributeError: 
            return False

        for purpose in purposes:
            if purpose in ('', 'default', 'normal'): 
                obj.SetBitmaps(bitmap, bitmap)
            elif purpose in ('checked',): 
                obj.SetBitmaps(bitmap, obj.GetBitmap(False))
            elif purpose in ('unchecked',): 
                obj.SetBitmaps(obj.GetBitmap(True), bitmap)
            else: 
                raise ValueError('Unknown purpose for image: \'%s\'' % purpose)

