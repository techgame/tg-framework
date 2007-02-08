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

# stdlib:
from gettext import gettext

# wxPython:
import wx

# TG: 

from TG.guiTools.wx import wxVersion, wxClasses
from TG.guiTools.wx import sizerTools
from TG.guiTools.wx import cssFont
from TG.guiTools.wx import colorDB
from TG.guiTools.wx.subjectEvtHandler import SubjectEvtHandler

from TG.skinning.common.css import CSSSkinElementInterface
from TG.skinning.common.cssElement import SkinElementCSSMixin
from TG.skinning.common.skin.compound import XMLSkin, CompoundElement, CompoundModelBase
from TG.skinning.common.python.inline import InlinePythonSkinElement

from __init__ import namespace

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Constants / Variables / Etc. 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = (
    'wx',
    'wxClasses',
    'wxVersion', 
    'namespace',

    'XMLSkin',

    'wxPySkinElementBase',

    'wxPyCompoundModel',
    'wxPySkinCompoundElement',
    'wxPySkinUnifiedCompoundElement', 
    'wxPySkinSeparateCompoundElement',

    'wxPySkinElement',
    'wxPyWidgetBaseSkinElement',
    'wxPostCreateWidgetMixin',
    'wxPyWindowSkinElement',
    'wxPyWidgetSkinElement',
    )

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Normalizations to wx 2.5.2
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if not hasattr(wx, 'FIXED_MINSIZE'):
    wx.FIXED_MINSIZE = 0 # this is a bit flag, so setting it to 0 should not affect anything

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CSSPySkinElementInterface(CSSSkinElementInterface):
    defaultCSSClass = ''

    def __init__(self, host, node, attributes, namespaceMap):
        CSSSkinElementInterface.__init__(self, host, node, attributes, namespaceMap)
        defaultCSSClass = host.getDefaultCSSClass()
        if defaultCSSClass:
            self.defaultCSSClass = defaultCSSClass

    def getClassAttr(self, default=''): 
        return (self.getAttr('css-class', None)
                or self.getAttr('class', None)
                or self.defaultCSSClass)

    def getStyleAttr(self):
        # style is already defined by wx
        return self.getAttr('css-style', '') 

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class KWDict(dict):
    def rename(self, *args, **kw):
        work = list(args)+kw.items()
        for to_, from_ in work:
            self[to_] = self.pop(from_)

class wxPySkinElementMixin(SkinElementCSSMixin):
    CSSElementInterfaceFactory = CSSPySkinElementInterface

    elementGlobals = vars(wx).copy()
    for key in elementGlobals.keys():
        if key[:2] == '__' and key[-2:] == '__':
            del elementGlobals[key]
    elementLocals = {'wx':wx, 'BestSize':wx.DefaultSize}

    defaultSettings = {}
    defaultStyleSettings = {}

    defaultCSSClass = None
    def getDefaultCSSClass(self):
        return self.defaultCSSClass

    def getSettingEval(self, name, default=NotImplemented, **kw):
        result = self.getSetting(name, default)
        if isinstance(result, basestring):
            result = self.evaluate(result, **kw)
        return result
    
    def getStyleSettingEval(self, name, default=NotImplemented, **kw):
        result = self.getStyleSetting(name, default)
        if isinstance(result, basestring):
            result = self.evaluate(result, **kw)
        elif isinstance(result, list):
            result = [self.evaluate(each, **kw) for each in result]
        return result

    def getStyleSettingLocalized(self, name, default=NotImplemented):
        result = self.getStyleSetting(name, default)
        return self.localizedText(result)
    def localizedText(self, text):
        ctxGetText = getattr(self.ctx, 'gettext', gettext)
        return ctxGetText(text)

    def getStyleColorSetting(self, name, default=None):
        color = self.getStyleSetting(name, default)
        if color:
            return self.getColorEval(color)
        else:
            return default

    def getColorEval(self, strColor):
        return colorDB.colorFromString(strColor, self.evaluate)

    def getStyleSettingsCollection(self, evaluate=(), normal=(), localized=(), kwStart={}, **kw):
        result = KWDict(kw)
        if kwStart: result.update(kwStart)

        sentinal = kw
        for each in evaluate: 
            eachResult = self.getStyleSettingEval(each, result.get(each, sentinal))
            if eachResult is not sentinal: 
                result[each] = eachResult 
        for each in normal: 
            eachResult = self.getStyleSetting(each, result.get(each, sentinal))
            if eachResult is not sentinal: 
                result[each] = eachResult 
        for each in localized: 
            eachResult = self.getStyleSettingLocalized(each, result.get(each, sentinal))
            if eachResult is not sentinal: 
                result[each] = eachResult 

        return result

    def getStyleSettingsCollectionWX(self, evaluate=(), *args, **kw):
        result = self.getStyleSettingsCollection(evaluate, *args, **kw)
        if 'style' in evaluate:
            addStyle = self.getStyleSettingEval('style-add', 0)
            removeStyle = self.getStyleSettingEval('style-remove', 0)
            if addStyle or removeStyle:
                result['style'] = (result.get('style', 0) & ~removeStyle) | addStyle
        result['id'] = self.getSettingEval('wxid')
        return result

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class wxPySkinElementBase(wxPySkinElementMixin, InlinePythonSkinElement):
    pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class wxPyCompoundModel(CompoundModelBase): 
    pass
class wxPySkinCompoundElement(CompoundElement, wxPySkinElementBase):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    defaultSettings = wxPySkinElementBase.defaultSettings.copy()
    defaultSettings.update(CompoundElement.defaultSettings)
    defaultSettings.update({
        })

    defaultStyleSettings = wxPySkinElementBase.defaultStyleSettings.copy()
    defaultStyleSettings.update({
        })

    CompoundModelFactory = wxPyCompoundModel
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def xmlInitStarted(self, elemBuilder):
        self._initChunks(elemBuilder)
        return CompoundElement.xmlInitStarted(self, elemBuilder)

    def xmlPreAddElement(self, elemBuilder, name, attributes, srcref):
        self._chunkContent(elemBuilder)
        return CompoundElement.xmlPreAddElement(self, elemBuilder, name, attributes, srcref)

    def xmlInitFinalized(self, elemBuilder):
        content, self.content = self.content, []
        try:
            result = CompoundElement.xmlInitFinalized(self, elemBuilder)
        finally:
            self.content = content
        self._chunkContent(elemBuilder, last=True)
        return result

    def xmlBuildComplete(self, elemBuilder):
        CompoundElement.xmlBuildComplete(self, elemBuilder)
        self._cleanupChunks(elemBuilder)

class wxPySkinUnifiedCompoundElement(CompoundElement.Unified, wxPySkinCompoundElement):
    pass
class wxPySkinSeparateCompoundElement(CompoundElement.Separate, wxPySkinCompoundElement):
    pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class wxPySkinElement(wxPySkinElementBase):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    defaultSettings = wxPySkinElementBase.defaultSettings.copy()
    defaultStyleSettings = wxPySkinElementBase.defaultStyleSettings.copy()

    windowTypes = wxClasses(wx.Window)
    frameTypes = wxClasses(wx.Frame, wx.Dialog, wx.MDIParentFrame)
    objParentTypes = windowTypes
    parentObj = None

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Definitions 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getParentFrame(self):
        return self.findXMLParentObjectOfType(self.frameTypes) or None
    def getApplication(self):
        return wx.GetApp()

    def getParentWindow(self):
        return self.findXMLParentObjectOfType(self.windowTypes)
    def getParentObj(self):
        if self.parentObj is None:
            self.parentObj = self._getParentObj()
        return self.parentObj
    def _getParentObj(self):
        if self.objParentTypes:
            return self.findXMLParentObjectOfType(self.objParentTypes) or None
        else: 
            return None
    def getParentOfObj(self):
        if self.objParentTypes:
            return self.findXMLParentOfType(self.objParentTypes) or None
        else: 
            return None

    def isWindowObj(self):
        return isinstance(self.getObject(), self.windowTypes)

    def isChildCollector(self): 
        return self.isWindowObj()
    def addCollectedChild(self, childElem, childObj): 
        return None

    def _getElemIfChildCollector(self, elem): 
        if isinstance(elem, wxPySkinElement):
            if elem.isChildCollector():
                return elem
        return None
    def findChildCollector(self):
        return self.findXMLParentsFor(self._getElemIfChildCollector)
    def registerWithCollector(self, obj):
        for collector in self.findChildCollector():
            if not collector.addCollectedChild(self, obj):
                break # break if we shouldn't continue looking up the stack

    def getLayoutObj(self):
        if self.isWindowObj():
            return self.getObject()
        else: return None

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def initialStandardOptions(self):
        obj = self.getObject()
        if obj is None: return
        if self.isWindowObj():
            self.initialStandardWindowOptions(obj)
            self.initialEventHandler(obj)

    def initialStandardWindowOptions(self, obj):
        # attrs related to size
        sizehints = self.getStyleSettingEval('size-hints', None)
        if sizehints:
            self.objSetSizeHints(obj, sizehints)

        virtualSize = self.getStyleSettingEval('size-virtual', None)
        if virtualSize:
            self.objSetVirtualSize(obj, virtualSize)

        if self.getStyleSetting('size') == 'BestSize':
            self.objSetBestSize(obj)

        # font and color styles
        font = self.getStyleFontSetting(None)
        if font:
            self.objSetFont(obj, font)
        fgColor = self.getStyleColorSetting('fgcolor', None)
        if fgColor is not None:
            obj.SetForegroundColour(fgColor)
        bgColor = self.getStyleColorSetting('bgcolor', None)
        if bgColor is not None:
            obj.SetBackgroundColour(bgColor)

        # windows generic
        extraStyle = self.getStyleSettingEval('style-extra', None)
        if extraStyle:
            self.objSetExtraStyle(obj, extraStyle)

        label = self.getStyleSetting('label', None)
        if label:
            self.objSetLabel(obj, label)
        tooltip = self.getStyleSetting('tooltip', None)
        if tooltip:
            tooltip = tooltip.decode("string_escape")
            obj.SetToolTipString(tooltip)
        help = self.getStyleSetting('help', None)
        if help:
            obj.SetHelpText(help)

        cursor = self.getStyleSettingEval('cursor', None)
        if cursor is not None:
            if isinstance(cursor, int):
                cursor = wx.StockCursor(cursor)
            obj.SetCursor(cursor)

    def initialEventHandler(self, obj):
        obj = self.getObject()
        SubjectEvtHandler.forEvtHandler(obj)

    def finalStandardOptions(self):
        obj = self.getObject()
        if obj is None: return

        self.registerWithCollector(obj)

        if self.isWindowObj():
            self.finalStandardWindowOptions(obj)

    def finalStandardWindowOptions(self, obj):
        autoLayout = self.getStyleSettingEval('size-autolayout', None)
        if autoLayout:
            obj.SetAutoLayout(autoLayout)

        enable = self.getStyleSettingEval('enable', None)
        if enable is not None:
            self.objEnable(obj, enable)

        show = self.getStyleSettingEval('show', None)
        if show is not None:
            self.objShow(obj, show)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    _fontStyleSettingKeys = ('font', 'font-family', 'font-size', 'font-style', 'font-variant', 'font-weight')
    def hasStyleFontSetting(self):
        return self.hasStyleSetting(forceCSS=True, *self._fontStyleSettingKeys)
    def getStyleFontSetting(self, default=wx.SYS_DEFAULT_GUI_FONT):
        kwFont = {}
        for key in self._fontStyleSettingKeys:
            value = self.getStyleSetting(key, None, forceCSS=True)
            if value is not None:
                kwFont[key] = value

        if self.parentObj is not None:
            parentFont = self.getParentObj().GetFont()
        else:
            anObj = self.getObject()
            if anObj:
                parentFont = anObj.GetFont()

        if kwFont:
            return cssFont.CSSFont.fromCSS(kwFont)
        else:
            if isinstance(default, (int, long)):
                default = wx.SystemSettings.GetFont(default)
            return default

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def objEnable(self, obj, show=True):
        """objEnable is broken out to allow for specialized code"""
        obj.Enable(show)
    def objShow(self, obj, show=True):
        """objShow is broken out to allow for specialized code"""
        obj.Show(show)
    def objSetLabel(self, obj, label=''):
        if label:
            obj.SetLabel(label)
    def objSetFont(self, obj, font):
        obj.SetFont(font)
    def objSetExtraStyle(self, obj, extraStyle):
        obj.SetExtraStyle(extraStyle)

    def objSetBestSize(self, obj):
        bestSize = obj.GetBestSize()
        obj.SetSize(bestSize)
    def objSetSizeHints(self, obj, sizehints):
        obj.SetSizeHints(*sizehints)
    def objSetVirtualSize(self, obj, virtualSize):
        obj.SetVirtualSize(virtualSize)
        obj.SetVirtualSizeHints(*virtualSize)

    def objSetSizer(self, obj, sizer, updateSizeHints=False, fitToSizer=False):
        obj.SetSizer(sizer)
        if updateSizeHints:
            sizerTools.adjustLayoutContainerSizes(obj, sizer)
        if fitToSizer:
            sizer.Fit(obj)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class wxPyWidgetBaseSkinElement(wxPySkinElement):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    defaultSettings = wxPySkinElement.defaultSettings.copy()
    defaultSettings.update({ 
        })

    defaultStyleSettings = wxPySkinElement.defaultStyleSettings.copy()
    defaultStyleSettings.update({
        })

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Definitions 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def xmlInitStarted(self, elemBuilder):
        wxPySkinElement.xmlInitStarted(self, elemBuilder)
        obj = self._tmCreateWidget()

    def xmlInitFinalized(self, elemBuilder):
        self._chunkContent(elemBuilder, last=False)
        obj = self._tmFinishWidget()
        wxPySkinElement.xmlInitFinalized(self, elemBuilder)

    def _tmAssureCreated(self):
        obj = wxPySkinElement.getObject(self)
        if obj is None: 
            self.parentObj = self.getParentObj()
            if self.parentObj is not None:
                obj = self._tmCreateWidget()
        return obj
    def _tmCreateWidget(self):
        """Template method to create the widget"""
        self.parentObj = self.getParentObj()
        obj = self.createWidget(self.parentObj)
        self.setObject(obj)
        self.initialStandardOptions()
        return obj
    def createWidget(self, parentObj):
        raise NotImplementedError, "Subclass responsibility"

    def _tmFinishWidget(self):
        """Template method to finish the widget"""
        obj = self.getObject()
        try:
            result = self.finishWidget(obj, self.parentObj)
        finally:
            if self.parentObj is not None:
                del self.parentObj

        if self.getObject() is None:
            self.setObject(result)

        self.finalStandardOptions()
        return obj
    def finishWidget(self, obj, parentObj):
        pass

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getLayoutMinSize(self):
        return self.getStyleSettingEval('layout-minsize', None)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class wxPostCreateWidgetMixin(wxPyWidgetBaseSkinElement):
    def xmlInitStarted(self, elemBuilder):
        # skip our direct base class...
        return wxPySkinElement.xmlInitStarted(self, elemBuilder)

    def xmlInitFinalized(self, elemBuilder):
        obj = self._tmAssureCreated()
        self._tmFinishWidget()
        return wxPySkinElement.xmlInitFinalized(self, elemBuilder)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class wxPyWindowSkinElement(wxPyWidgetBaseSkinElement):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    defaultSettings = wxPyWidgetBaseSkinElement.defaultSettings.copy()
    defaultSettings.update({ 
        'wxid': 'NewId()',
        })

    defaultStyleSettings = wxPyWidgetBaseSkinElement.defaultStyleSettings.copy()
    defaultStyleSettings.update({
        #'style': '0',
        #'style-add': '0',
        #'style-remove': '0',
        'size': 'DefaultSize',
        'pos': 'DefaultPosition',
        })

    def getLayoutObj(self):
        return None # Top-level windows do not participate in layouts

    def _getParentObj(self):
        parentObj = self.getParentFrame()
        if parentObj is None:
            if not self.getStyleSettingEval('frame-main'):
                parentObj = self.getApplication().GetTopWindow()
        return parentObj

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class wxPyWidgetSkinElement(wxPyWidgetBaseSkinElement):
    defaultSettings = wxPyWidgetBaseSkinElement.defaultSettings.copy()
    defaultSettings.update({
        'wxid': 'NewId()',
        })

    defaultStyleSettings = wxPyWidgetBaseSkinElement.defaultStyleSettings.copy()
    defaultStyleSettings.update({
        #'style': '0',
        #'style-add': '0',
        #'style-remove': '0',
        'size': 'DefaultSize',
        'pos': 'DefaultPosition',
        'layout-minsize': 'None',
        })

