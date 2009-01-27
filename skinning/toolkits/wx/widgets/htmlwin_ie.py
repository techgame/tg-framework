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

from TG.guiTools.wx.subjectEvtHandler import SubjectEvtHandler
from TG.skinning.toolkits.wx._baseElements import *
from TG.skinning.engine.xmlSkinner import XMLFactory
from TG.w3c import xmlNode
from wx.lib import iewin

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class htmlwin_ie(wxPyWidgetSkinElement):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    elementGlobals = wxPyWidgetSkinElement.elementGlobals.copy()
    elementGlobals.update(vars(iewin))

    defaultSettings = wxPyWidgetSkinElement.defaultSettings.copy()
    defaultSettings.update({ 
        })

    defaultStyleSettings = wxPyWidgetSkinElement.defaultStyleSettings.copy()
    defaultStyleSettings.update({
        'style':    '0',
        'ref': '',
        })

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Definitions 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def createWidget(self, parentObj):
        kwWX = self.getStyleSettingsCollectionWX(('style', 'pos', 'size'))
        kwWX.rename(('ID', 'id'))
        obj = iewin.IEHtmlWindow(parentObj, **kwWX)
        self.setObject(obj)
        self.HtmlWindowOptions()
        return obj

    def finishWidget(self, obj, parentObj):
        if self.getChildren():
            self.updateFromChildren(obj, parentObj)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getEvtHandler(self):
        # Seems to send the events to the frame... so...
        evtHandler = self.getParentFrame()
        return SubjectEvtHandler.forEvtHandler(evtHandler)
    def installDefaultEvent(self, evtHandler, evtObject, evtCallback):
        iewin.EVT_BeforeNavigate2(evtHandler, -1, evtCallback)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def HtmlWindowOptions(self):
        obj = self.getObject()

        ref = self.getStyleSettingRef()
        if ref:
            # Translate the ref to a local resource, if applicable
            resource = self.getURIResolver().resolve(ref, default=None)
            if resource:
                ref = resource.getURI()
            if ref:
                # Load the page at the next "available" time
                wx.CallAfter(obj.LoadUrl, ref)

    def updateFromChildren(self, obj, parentObj):
        pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class htmlwin_ie_WithSource(htmlwin_ie):
    # Todo: When we know how to the source of the IEHtmlWindow, this can be reintegrated
    # Note: origionally from "htmlwin"

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    xmlFactories = XMLFactory.Collection({
        ('http://www.w3.org/1999/xhtml',): xmlNode.XMLNodeFactory(),
        (None, 'html'): xmlNode.XMLNodeFactory(),
        (None, 'body'): xmlNode.XMLNodeFactory(),
        None: xmlNode.XMLNodeFactory(),
        }).setName('htmlwin-ie')


    defaultSettings = htmlwin_ie.defaultSettings.copy()
    defaultSettings.update({ 
        })

    defaultStyleSettings = htmlwin_ie.defaultStyleSettings.copy()
    defaultStyleSettings.update({
        'src': 'None',
        })

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Definitions 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def xmlInitStarted(self, elemBuilder):
        result = htmlwin_ie.xmlInitStarted(self, elemBuilder)
        elemBuilder.pushXMLFactories(self.xmlFactories)
        return result

    def xmlInitFinalized(self, elemBuilder):
        htmlwin_ie.xmlInitFinalized(self, elemBuilder)
        elemBuilder.popXMLFactories()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def HtmlWindowOptions(self):
        htmlwin_ie.HtmlWindowOptions(self)

        src = self.getStyleSettingEval('src')
        if src:
            obj.SetPage(src)
            
    def updateFromChildren(self, obj, parentObj):
        if len(self.getChildren()) > 1:
            html = xmlNode.XMLNode('html')
            for child in self.getChildren():
                html.addNode(child)
        else:
            html, = self.getChildren()
        obj.SetPage(html.toXML())

