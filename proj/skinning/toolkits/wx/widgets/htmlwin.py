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

import wx.html
from TG.guiTools.wx import htmlEvents
from TG.skinning.toolkits.wx._baseElements import *
from TG.skinning.engine.xmlSkinner import XMLFactory
from TG.w3c import xmlNode

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class htmlwin(wxPyWidgetSkinElement):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    elementGlobals = wxPyWidgetSkinElement.elementGlobals.copy()
    elementGlobals.update(vars(wx.html))
    elementGlobals.update(vars(htmlEvents))

    xmlFactories = XMLFactory.Collection({
        ('http://www.w3.org/1999/xhtml',): xmlNode.XMLNodeFactory(),
        ('xhtml',): xmlNode.XMLNodeFactory(),
        ('html',): xmlNode.XMLNodeFactory(),
        None: xmlNode.XMLNodeFactory(),
        }).setName('htmlwin')
    defaultSettings = wxPyWidgetSkinElement.defaultSettings.copy()
    defaultSettings.update({ 
        })

    defaultStyleSettings = wxPyWidgetSkinElement.defaultStyleSettings.copy()
    defaultStyleSettings.update({
        'size':'200,200',
        'borders': 'None',
        'src': 'None',
        'ref': '',
        })

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Definitions 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def xmlInitStarted(self, elemBuilder):
        result = wxPyWidgetSkinElement.xmlInitStarted(self, elemBuilder)
        xmlFactories = elemBuilder.xmlFactories.copy()
        xmlFactories.update(self.xmlFactories)
        elemBuilder.pushXMLFactories(xmlFactories)
        return result

    def xmlInitFinalized(self, elemBuilder):
        elemBuilder.popXMLFactories()
        return wxPyWidgetSkinElement.xmlInitFinalized(self, elemBuilder)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def createWidget(self, parentObj):
        kwWX = self.getStyleSettingsCollectionWX(('style', 'pos', 'size'))
        obj = htmlEvents.HtmlWindowWithEvents(parentObj, **kwWX)
        self.setObject(obj)
        self.htmlWindowOptions(obj)
        return obj

    def finishWidget(self, obj, parentObj):
        if self.getChildren():
            self.updateFromChildren(obj, parentObj)

    def installDefaultEvent(self, evtHandler, evtObject, evtCallback):
        htmlEvents.EVT_HTMLWIN_LINK(evtHandler, evtObject.GetId(), evtCallback)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def htmlWindowOptions(self, obj):
        border = self.getStyleSettingEval('borders')
        if border is not None:
            obj.SetBorders(border)

        src = self.getStyleSettingEval('src')
        if src is not None:
            obj.SetPage(src)
            
        ref = self.getStyleSettingRef()
        if ref:
            # Translate the ref to a local resource, if applicable
            resource = self.getURIResolver().resolve(ref, default=None)
            if resource:
                ref = resource.getURI()
            if ref: 
                # The app was hanging when the following was called
                # directly... so just delay it until the next "available" time
                wx.CallAfter(obj.LoadPage, ref)

    def updateFromChildren(self, obj, parentObj):
        htmlchildren = [child for child in self.getChildren() if isinstance(child, xmlNode.XMLNode)]
        if len(htmlchildren) == 1:
            html, = htmlchildren
        elif len(htmlchildren) > 1:
            html = xmlNode.XMLNode('html')
            for child in htmlchildren:
                html.addNode(child)
        else:
            html = None

        if html is not None:
            obj.SetPage(html.toXML())

