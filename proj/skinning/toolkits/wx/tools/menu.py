#!/sr/bin/env python
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

from TG.skinning.engine.xmlSkinner import XMLFactory
from TG.skinning.toolkits.wx._baseElements import *
from TG.guiTools.wx.subjectEvtHandler import SubjectEvtHandler

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Menu Element 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MenuCommon(wxPyWidgetBaseSkinElement):
    objParentTypes = wxClasses(wx.MenuBar, wx.Menu)
    menubarParentType = wxClasses(wx.MenuBar)
    menuParentType = wxClasses(wx.Menu)

    def getEvtHandler(self):
        evtHandler = self.getSettingEval('evt-handler', None)
        if evtHandler is None:
            if self.findXMLParentObjectOfType(self.menubarParentType) is not None:
                evtHandler = self.getParentFrame()
            else: 
                try:
                    getEvtHandler = self.xmlParent().getEvtHandler
                except AttributeError:
                    evtHandler = self.getParentObj()
                else:
                    evtHandler = getEvtHandler()

            if evtHandler is None:
                evtHandler = self.getObject()

        return SubjectEvtHandler.forEvtHandler(evtHandler)

    def installDefaultEvent(self, evtHandler, evtObject, evtCallback):
        pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class GroupMenuBase(MenuCommon):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    defaultSettings = MenuCommon.defaultSettings.copy()
    defaultSettings.update({ 
        'wxid':'NewId()',
        })

    defaultStyleSettings = MenuCommon.defaultStyleSettings.copy()
    defaultStyleSettings.update({
        'style': '0',
        'title': '',
        'text': 'Menu',
        'help': '',
        'index': 'None',
        })

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Definitions 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def createWidget(self, parentObj):
        kwWX = self.getStyleSettingsCollectionWX(('style',), localized=('title',))
        wxid = kwWX.pop('id', -1)
        obj = wx.Menu(**kwWX)
        obj.wxid = wxid
        return obj

    def finishWidget(self, obj, parentObj):
        index = self.getStyleSettingEval('index')
        obj.text = self.getStyleSettingLocalized('text')
        obj.help = self.getStyleSettingLocalized('help')
        if isinstance(parentObj, self.menubarParentType):
            if index is None:
                parentObj.Append(obj, obj.text)
            else:
                parentObj.Insert(index, obj, obj.text)
        elif isinstance(parentObj, self.menuParentType):
            if index is None:
                parentObj.AppendMenu(obj.wxid, obj.text, obj, obj.help) 
            else:
                parentObj.InsertMenu(index, obj.wxid, obj.text, obj, obj.help)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Local import to avoid circular references
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import menu_item
import menu_break

class menu(GroupMenuBase):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    xmlFactories = XMLFactory.Collection({
        (namespace, 'item'): XMLFactory.Static(menu_item.menu_item),
        (namespace, 'break'): XMLFactory.Static(menu_break.menu_break),
        (namespace, 'menu'): XMLFactory.Static(GroupMenuBase),

        None: XMLFactory.InheritFromNext(),
        }).setName('menu')

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Definitions 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def xmlInitStarted(self, elemBuilder):
        result = GroupMenuBase.xmlInitStarted(self, elemBuilder)
        elemBuilder.pushXMLFactories(self.xmlFactories)
        return result

    def xmlInitFinalized(self, elemBuilder):
        GroupMenuBase.xmlInitFinalized(self, elemBuilder)
        elemBuilder.popXMLFactories()

