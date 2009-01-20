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

from htmlwin import *
from TG.skinning.common.skin import reference, store

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class wxPySkinTagHandler(wx.html.HtmlWinTagHandler):
    """Derived from wx.lib.wxpTag written by Robin Dunn and adapted to
    the TG.skinning.toolkits.wx framework."""

    skinTags = ['wxPy','wxPySkin']
    skinTags = [tag.upper() for tag in skinTags]# Required for wx.HtmlWinTagHandler

    def GetSupportedTags(self):
        return ','.join(self.skinTags)

    def HandleTag(self, tag):
        tagname = tag.GetName()
        if tagname not in self.skinTags:
            raise ValueError, 'Tag %s not supported by %s' % (tagname, self.__class__.__name__)
        else:
            container = self.GetParser().GetContainer()
            if not container: 
                return False
            window = self.GetParser().GetWindow()
            if not window: 
                return False
            skinElem = window.skinElem()
            if not skinElem: 
                return False

            # Load the skin representing this tag
            for cell in skinElem.loadCellsForTag(tag):
                if cell is not None:
                    container.InsertCell(cell)
            return True

    def AddTagHandler(klass): 
        wx.html.HtmlWinParser_AddTagHandler(klass)
    AddTagHandler = classmethod(AddTagHandler)

wxPySkinTagHandler.AddTagHandler()

class htmlwin_skin(htmlwin):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    defaultSettings = htmlwin.defaultSettings.copy()
    defaultSettings.update({ 
        'ctx-push':'1',
        })

    defaultStyleSettings = htmlwin.defaultStyleSettings.copy()
    defaultStyleSettings.update({
        })

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Definitions 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def createWidget(self, parentObj):
        #self.pushContext()
        obj = htmlwin.createWidget(self, parentObj)
        obj.skinElem = self.asWeakRef()
        return obj

    def finishWidget(self, obj, parentObj):
        return htmlwin.finishWidget(self, obj, parentObj)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def xmlInitStarted(self, elemBuilder):
        self.wrElemBuilder = elemBuilder.asWeakRef()
        return htmlwin.xmlInitStarted(self, elemBuilder)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def updateFromChildren(self, obj, parentObj):
        for child in self.getChildren():
            if isinstance(child, xmlNode.XMLNode):
                obj.SetPage(child.toXML())

    #~ to handle tags for wx skinning framework ~~~~~~~~~

    def loadCellsForTag(self, tag):
        skinElem, children = self.loadSkinForTag(self, tag)
        if skinElem is None:
            return

        for child in children:
            childObj = child.getObject()
            if isinstance(childObj, self.windowTypes):
                childObj.Layout()

                if tag.HasParam('width'):
                    width = int(tag.GetParam('width'))
                else: width = 0

                # Load the SkinObject into a html widget cell
                cell = wx.html.HtmlWidgetCell(childObj, width)
                yield cell

    def loadSkinForTag(self, taghandler, tag):
        elemBuilder = self.wrElemBuilder()

        oldChildren = self.setChildren([]) 
        try:
            # Determine if the tag is a reference or a skin invokation
            if tag.HasParam('ref'):
                skinFilename = tag.GetParam('ref')
                result = self.referenceSkinFile(elemBuilder, skinFilename)
            elif tag.HasParam('href'):
                skinFilename = tag.GetParam('href')
                result = self.referenceSkinFile(elemBuilder, skinFilename)
            elif tag.HasParam('invoke'):
                invokeName = tag.GetParam('invoke')
                result = self.templateInvoke(elemBuilder, invokeName)
            else:
                result = None
        finally:
            children = self.setChildren(oldChildren)
        return result, children

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Utilities
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def templateInvoke(self, elemBuilder, invokeName):
        templateOuter = self.getContextVar(invokeName)
        self.invokeRestoreable(elemBuilder, templateOuter)
        return templateOuter

    invokeRestoreable = store.invokeRestoreable

    referenceSkin = reference.referenceSkin
    referenceSkinFile = reference.referenceSkinFile
    referenceSkinParseContext = reference.referenceSkinParseContext

