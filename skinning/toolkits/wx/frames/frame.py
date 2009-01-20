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

from TG.common.utilities import boolFromStr
from TG.guiTools.wx import lockingFrame
from TG.guiTools.wx.lockingFrame import LockingFrameMixin, LockSide

from TG.skinning.toolkits.wx._baseElements import *
from TG.skinning.toolkits.wx.tools import image

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class frame(image.BitmapImageHandlerMixin, wxPyWindowSkinElement):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    defaultCSSClass = 'frame'
    _ctxHostObjNames = ('frame', )

    elementLocals = wxPyWindowSkinElement.elementLocals .copy()
    elementLocals['lockWindowsTogether'] = lockingFrame.lockWindowsTogether
    elementLocals['lockToDesktop'] = lockingFrame.lockToDesktop

    defaultSettings = wxPyWindowSkinElement.defaultSettings.copy()
    defaultSettings.update({ 
        'ctx-push':'True',
        })

    defaultStyleSettings = wxPyWindowSkinElement.defaultStyleSettings.copy()
    defaultStyleSettings.update({
        'style': 'DEFAULT_FRAME_STYLE | CLIP_CHILDREN',
        'title': 'Frame',
        'frame-top': 'False',
        'frame-main': 'True',
        'locking': 'None',
        'fullscreen': 'None',
        })

    objParentTypes = wxPyWindowSkinElement.frameTypes

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Definitions 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def createWidget(self, parentObj):
        obj = self.createFrame(parentObj)
        if self.getStyleSettingEval('frame-top'):
            self.ctx.application.SetTopWindow(obj)
        return obj

    def finishWidget(self, obj, parentObj):
        self.finishFrame(obj, parentObj)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getFrameKW(self):
        return self.getStyleSettingsCollectionWX(('style', 'pos', 'size'), localized=('title',))

    def createFrame(self, parentObj, frameKlass=wx.Frame):
        kwWX = self.getFrameKW()
        locking = self.getStyleSetting('locking')
        if not boolFromStr(locking):
            result = frameKlass(parentObj,**kwWX)
        else:
            result = LockingFrameMixin.mixedWith(frameKlass)(parentObj, **kwWX)
            if ',' in locking:
                locking = self.evaluate(locking)
            elif locking.lower() not in LockSide.LockingStyles:
                locking = 'standard'
            result.setLockingStyle(locking)
        return result

    def finishFrame(self, obj, parentObj):
        obj.Layout()

    def installDefaultEvent(self, evtHandler, evtObject, evtCallback):
        wx.EVT_CLOSE(evtHandler, evtCallback)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def finalStandardWindowOptions(self, obj):
        result = wxPyWindowSkinElement.finalStandardWindowOptions(self, obj)

        fullscreen = self.getStyleSettingEval('fullscreen')
        if fullscreen:
            if fullscreen < 0 or fullscreen is True:
                fullscreen = wx.FULLSCREEN_ALL
            obj.ShowFullScreen(True, fullscreen)

        return result

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def lockToSelf(self, frame, LockSideIndicies=(LockSide.bottom,LockSide.innerLeft), LockSizeIndicies=()):
        return lockingFrame.lockWindowsTogether(self.getObject(), frame, LockSideIndicies, LockSizeIndicies)
    lockFrameToSelf = lockToSelf

    def lockTo(self, frame, LockSideIndicies=(LockSide.bottom,LockSide.innerLeft), LockSizeIndicies=()):
        return lockingFrame.lockWindowsTogether(frame, self.getObject(), LockSideIndicies, LockSizeIndicies)
    lockToFrame = lockTo

    def lockToDesktop(self, LockSideIndicies=(LockSide.innerTop,LockSide.innerLeft), LockSizeIndicies=()):
        return lockingFrame.lockToDesktop(self.getObject(), LockSideIndicies, LockSizeIndicies)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def addCollectedBitmapChild(self, childElem, bitmap, purposes):
        for purpose in purposes:
            if purpose in ('icon',): 
                self.setFrameIcon(bitmap)
            elif purpose in ('shape'): 
                self.setFrameShape(childElem.getObject(), bitmap)
            else: 
                raise ValueError('Unknown purpose for image: \'%s\'' % purpose)

    def setFrameIcon(self, bitmap):
        icon = wx.IconFromBitmap(bitmap)
        self.getObject().SetIcon(icon)

    def setFrameShape(self, image, bitmap):
        if not bitmap.GetMask():
            mask = wx.MaskColour(bitmap, wx.Color(image.GetRed(0,0), image.GetGreen(0,0), image.GetBlue(0,0)))
            bitmap.SetMask(mask)

        obj = self.getObject()
        obj.SetShape(wx.RegionFromBitmap(bitmap))
        obj.SetSize((bitmap.GetWidth(), bitmap.GetHeight()))

