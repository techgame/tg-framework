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

import wx.xrc
from TG.skinning.toolkits.wx._baseElements import *
from TG.skinning.engine.xmlSkinner import XMLFactory
from TG.w3c import xmlNode

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class xrc(wxPyWidgetSkinElement):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    xmlFactories = XMLFactory.Collection({
        None: xmlNode.XMLNodeFactory(),
        }).setName('xrc')

    defaultSettings = wxPyWidgetSkinElement.defaultSettings.copy()
    defaultSettings.update({ 
        })

    defaultStyleSettings = wxPyWidgetSkinElement.defaultStyleSettings.copy()
    defaultStyleSettings.update({
        'name': 'root',
        'ref': '',
        })

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Definitions 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def xmlInitStarted(self, elemBuilder):
        result = wxPyWidgetSkinElement.xmlInitStarted(self, elemBuilder)
        elemBuilder.pushXMLFactories(self.xmlFactories)
        return result

    def xmlInitFinalized(self, elemBuilder):
        elemBuilder.popXMLFactories()
        return wxPyWidgetSkinElement.xmlInitFinalized(self, elemBuilder)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def createWidget(self, parentObj):
        ref = self.getStyleSettingRef()
        if ref:
            xrc = self.getXRCFromRef(ref)
            return self.loadXRCResource(parentObj, xrc)
        else:
            return None

    def finishWidget(self, obj, parentObj):
        if obj is None:
            xrc = self.getXRCFromChildren(self.getChildren())
            obj = self.loadXRCResource(parentObj, xrc)
            self.setObject(obj)
            self.initialStandardOptions()

    def loadXRCResource(self, parentObj, xrc):
        resource = wx.xrc.EmptyXmlResource()
        resource.LoadFromString(xrc)
        name = self.getStyleSetting('name')
        return self.loadFromResource(resource, parentObj, name)

    def loadFromResource(self, resource, parentObj, name):
        raise NotImplementedError, "Need to determine how to generically load from resource"

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getXRCFromChildren(self, children):
        xrcchildren = [child for child in children if isinstance(child, xmlNode.XMLNode)]
        if len(xrcchildren) == 1:
            xrc, = xrcchildren
        elif len(xrcchildren) > 1:
            xrc = xmlNode.XMLNode('resource')
            for child in xrcchildren:
                xrc.addNode(child)
        else:
            xrc = None

        if xrc is not None:
            return xrc.toXML()

    def getXRCFromRef(self, ref):
        resource = self.getURIResolver().resolve(ref)
        resourceFile = resource.open('rb')
        try: 
            xrc = resourceFile.read()
        finally: 
            resourceFile.close()
        return xrc
