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
from TG.skinning.toolkits.wx.tools import image
import wx.wizard

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SkinWizardPage(wx.wizard.PyWizardPage):
    _next = None
    _prev = None
    _bitmap = wx.NullBitmap
    _resource = None

    def __init__(self, parent=None, prev=None, next=None, bitmap=None, resource=None, label=None):
        if bitmap is not None:
            self.SetBitmap(bitmap)
        if resource:
            self.SetResource(resource)

        wx.wizard.PyWizardPage.__init__(self, parent, self.GetBitmap())
        if label:
            self.SetLabel(label)

        if prev is not None:
            self.SetPrev(prev)
        if next is not None:
            self.SetNext(next)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def GetNext(self):
        if self._next is None and self.isDynamic():
            return self
        return self._next
    def SetNext(self, next, chain=True, onlyIfUnset=False):
        if isinstance(next, tuple):
            next, chain = next

        if onlyIfUnset: 
            if self._next is None:
                self._next = next
            return

        self._next = next

        if chain and next is not None:
            next.SetPrev(self, onlyIfUnset=True)

    def GetPrev(self):
        return self._prev
    def SetPrev(self, prev, chain=True, onlyIfUnset=False):
        if isinstance(prev, tuple):
            prev, chain = prev

        if onlyIfUnset: 
            if self._prev is None:
                self._prev = prev
            return

        self._prev = prev

        if chain and prev is not None:
            prev.SetNext(self, onlyIfUnset=True)

    def GetBitmap(self):
        return self._bitmap
    def SetBitmap(self, bitmap):
        if bitmap is None:
            bitmap = wx.NullBitmap
        self._bitmap = bitmap

    def GetResource(self):
        return self._resource
    def SetResource(self, resource):
        self._resource = resource

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    _isDynamic = None
    def isDynamic(self):
        return bool(self._isDynamic)
    def setDynamic(self, isDynamic=True):
        self._isDynamic = isDynamic

    _firstPage = False
    def isFirstPage(self):
        return bool(self._firstPage)
    def setFirstPage(self, firstPage=True):
        self._firstPage = firstPage

    _finalPage = False
    def isFinalPage(self):
        return bool(self._finalPage)
    def setFinalPage(self, finalPage=True):
        self._finalPage = finalPage

    _prevEnabled = None
    def isPrevEnabled(self):
        if self._prevEnabled is None:
            return bool(self._prev) or not self.isFirstPage()
        else: return bool(self._prevEnabled)
    def setPrevEnabled(self, bPrevEnabled=True):
        self._prevEnabled = bool(bPrevEnabled)
    def delPrevEnabled(self):
        self._prevEnabled = None

    _nextEnabled = None
    def isNextEnabled(self):
        if self._nextEnabled is None:
            return bool(self._next) or self.isFinalPage()
        else: return bool(self._nextEnabled)
    def setNextEnabled(self, bNextEnabled=True):
        self._nextEnabled = bool(bNextEnabled)
    def delNextEnabled(self):
        self._nextEnabled = None

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class wizard_page(image.BitmapImageHandlerMixin, wxPyWidgetSkinElement):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    elementGlobals = wxPyWidgetSkinElement.elementGlobals.copy()
    elementGlobals.update(vars(wx.wizard))

    defaultSettings = wxPyWidgetSkinElement.defaultSettings.copy()
    defaultSettings.update({ 
        })

    defaultStyleSettings = wxPyWidgetSkinElement.defaultStyleSettings.copy()
    defaultStyleSettings.update({
        'resource': '',
        'prev': 'None',
        'next': 'None',
        'dynamic': 'False',
        })

    objParentTypes = wxClasses(wx.wizard.Wizard)
    _ctxHostObjNames = ('wizardPage',)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Definitions 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def createWidget(self, parentObj):
        kw = self.getStyleSettingsCollection(('prev', 'next'), ('resource',), localized=('label',))
        obj = SkinWizardPage(parentObj, **kw)
        obj.setDynamic(self.getStyleSettingEval('dynamic'))
        return obj

    def finishWidget(self, obj, parentObj):
        pass

    def addCollectedBitmapChild(self, childElem, bitmap, purposes):
        obj = self.getObject()
        for purpose in purposes:
            if purpose in ('', 'default', 'normal'): 
                obj.SetBitmap(bitmap)
            elif purpose in ('none',): 
                pass
            else: 
                raise ValueError('Unknown purpose for image: \'%s\'' % purpose)

