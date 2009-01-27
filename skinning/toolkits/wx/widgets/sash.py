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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SkinSashLayoutWindow(wx.SashLayoutWindow):
    sashLayout = None

    def Show(self, *args, **kw):
        result = wx.SashLayoutWindow.Show(self, *args, **kw)
        self.update()
        return result
    def Hide(self, *args, **kw):
        result = wx.SashLayoutWindow.Hide(self, *args, **kw)
        self.update()
        return result
    def SetDefaultSize(self, *args, **kw):
        result = wx.SashLayoutWindow.SetDefaultSize(self, *args, **kw)
        self.update()
        return result

    def SendSizeEvent(self):
        # This method is called from ../docking/dock_host_sash.py
        # to get repaint events to work right
        w,h = self.GetClientSize()
        self.SetClientSize((w+1, h+1))
        self.SetClientSize((w, h))

    def update(self):
        sashLayout = self.getSashLayout()
        if sashLayout is not None:
            sashLayout.Layout()

    def getSashLayout(self):
        return self.sashLayout
    def setSashLayout(self, sashLayout):
        self.sashLayout = sashLayout
    
    def onSashDragged(self, evt):
        if evt.GetDragStatus() != wx.SASH_STATUS_OUT_OF_RANGE:
            self.SetDefaultSize(evt.GetDragRect().GetSize())

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class sash(wxPyWidgetSkinElement):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    elementLocals = wxPyWidgetSkinElement.elementLocals.copy()
    elementLocals.update({
        'left':wx.LAYOUT_LEFT, 
        'right':wx.LAYOUT_RIGHT, 
        'top':wx.LAYOUT_TOP, 
        'bottom':wx.LAYOUT_BOTTOM,

        'horizontal':wx.LAYOUT_HORIZONTAL,
        'vertical':wx.LAYOUT_VERTICAL,
        'horiz':wx.LAYOUT_HORIZONTAL,
        'vert':wx.LAYOUT_VERTICAL,

        'auto':'auto',
        'none':None,
        })

    defaultSettings = wxPyWidgetSkinElement.defaultSettings.copy()
    defaultSettings.update({ 
        })

    defaultStyleSettings = wxPyWidgetSkinElement.defaultStyleSettings.copy()
    defaultStyleSettings.update({
        'style': 'CLIP_CHILDREN|SW_3D',
        'autosize': 'True',
        'autodrag': 'True',

        'align': 'left',
        'orient': 'auto',

        'edges': 'auto',
        'size-border': 'None',
        'size-border-all': 'None',

        'x-range': '0, None',
        'y-range': '0, None',
        })

    edgeAutoAlignMap = {
        wx.LAYOUT_LEFT: wx.SASH_RIGHT,
        wx.LAYOUT_RIGHT: wx.SASH_LEFT,
        wx.LAYOUT_TOP: wx.SASH_BOTTOM,
        wx.LAYOUT_BOTTOM: wx.SASH_TOP,
        }

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Definitions 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def createWidget(self, parentObj):
        kwWX = self.getStyleSettingsCollectionWX(('style', 'pos', 'size'))
        obj = SkinSashLayoutWindow(parentObj, **kwWX)
        self.initialSashSettings(obj)
        return obj

    def finishWidget(self, obj, parentObj):
        pass

    def installDefaultEvent(self, evtHandler, evtObject, evtCallback):
        wx.EVT_SASH_DRAGGED(evtHandler, evtObject.GetId(), evtCallback)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def isChildCollector(self):
        return True
    def addCollectedChild(self, childElem, childObj): 
        if isinstance(childObj, self.windowTypes):
            if self.getStyleSettingEval('autosize'):
                self.getObject().SetDefaultSize(childObj.GetBestSize())

        return wxPyWidgetSkinElement.addCollectedChild(self, childElem, childObj) 
        
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def initialSashSettings(self, obj=None):
        if obj is None: obj = self.getObject()
        self.setSashLayout(obj)
        self.setSashRangeSettings(obj)
        self.setSashEdgeSettings(obj)

    def setSashLayout(self, obj):
        align = self.getStyleSettingEval('align')
        orient = self.getStyleSettingEval('orient')
        if orient == 'auto':
            if align in (wx.LAYOUT_LEFT, wx.LAYOUT_RIGHT):
                orient = wx.LAYOUT_VERTICAL
            elif align in (wx.LAYOUT_TOP, wx.LAYOUT_BOTTOM):
                orient = wx.LAYOUT_HORIZONTAL
        obj.SetAlignment(align)
        obj.SetOrientation(orient)
        if not self.getStyleSettingEval('autosize'):
            obj.SetDefaultSize(self.getStyleSettingEval('size'))

        if self.getStyleSettingEval('autodrag'):
            wx.EVT_SASH_DRAGGED(obj, obj.GetId(), obj.onSashDragged)

    def setSashRangeSettings(self, obj):
        xmin, xmax = self.getStyleSettingEval('x-range')
        if xmin is not None: 
            obj.SetMinimumSizeX(xmin)
        if xmax is not None: 
            obj.SetMaximumSizeX(xmax)

        ymin, ymax = self.getStyleSettingEval('y-range')
        if ymin is not None: 
            obj.SetMinimumSizeY(ymin)
        if ymax is not None: 
            obj.SetMaximumSizeY(ymax)

    def setSashEdgeSettings(self, obj):
        edges = self.getStyleSettingEval('edges')
        if edges == 'auto':
            edges = self.edgeAutoAlignMap[obj.GetAlignment()],
        elif isinstance(edges, int): 
            edges = edges,
        elif edges is None: 
            edges = ()
        for edge in edges:
            obj.SetSashVisible(edge, True)

        borderSize = self.getStyleSettingEval('size-border')
        if borderSize is not None:
            obj.SetDefaultBorderSize(borderSize)
        extraBorderSize = self.getStyleSettingEval('size-border-all')
        if extraBorderSize is not None:
            obj.SetExtraBorderSize(extraBorderSize)

