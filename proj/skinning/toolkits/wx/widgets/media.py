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
from  wx.media import MediaCtrl, MEDIACTRLPLAYERCONTROLS_NONE, MEDIACTRLPLAYERCONTROLS_DEFAULT, MEDIACTRLPLAYERCONTROLS_STEP
import wx.media
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class media(wxPyWidgetSkinElement):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    elementGlobals = wxPyWidgetSkinElement.elementGlobals.copy()
    elementGlobals.update(vars(wx.media))

    defaultSettings = wxPyWidgetSkinElement.defaultSettings.copy()
    defaultSettings.update({ 
        })

    defaultStyleSettings = wxPyWidgetSkinElement.defaultStyleSettings.copy()
    defaultStyleSettings.update({
        'backend': 'u""',
        'bestfit': True,
        'playercontrols': False,
        })

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Definitions 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def createWidget(self, parentObj):
        
        kwWX = self.getStyleSettingsCollectionWX(('style', 'pos', 'size', 'backend'), )
        kwWX.rename(szBackend='backend')
        playercontrols = self.getStyleSettingEval('playercontrols')


        #Create(self, Window parent, int id=-1, String fileName=EmptyString, 
        #    Point pos=DefaultPosition, Size size=DefaultSize, 
        #    long style=0, String szBackend=EmptyString, 
        #    Validator validator=DefaultValidator, 
        #    String name=MediaCtrlNameStr) -> bool
        obj = MediaCtrl(parentObj, **kwWX)

        if playercontrols:
            obj.ShowPlayerControls(MEDIACTRLPLAYERCONTROLS_DEFAULT)

        if self.getStyleSettingEval('bestfit', False):
            obj.SetBestFittingSize()
        
        return obj

    def finishWidget(self, obj, parentObj):
        pass

    def installDefaultEvent(self, evtHandler, evtObject, evtCallback):
        if hasattr(wx.media, 'EVT_MEDIA_STATECHANGED'):
            wx.media.EVT_MEDIA_STATECHANGED(evtHandler, evtObject.GetId(), evtCallback)
        else:
            wx.media.EVT_MEDIA_LOADED(evtHandler, evtObject.GetId(), evtCallback)


