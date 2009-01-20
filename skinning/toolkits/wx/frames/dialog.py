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

from frame import *

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class dialog(frame):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    _ctxHostObjNames = ('frame', 'dialog')

    elementLocals = frame.elementLocals .copy()
    elementLocals.update(modal='modal')
    
    defaultSettings = frame.defaultSettings.copy()
    defaultSettings.update({ 
        })

    defaultStyleSettings = frame.defaultStyleSettings.copy()
    defaultStyleSettings.update({
        'style': 'DEFAULT_DIALOG_STYLE | CLIP_CHILDREN',
        'style-extra': 'WS_EX_VALIDATE_RECURSIVELY',
        'title': 'Dialog',
        })

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Definitions 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def createFrame(self, winParent):
        return frame.createFrame(self, winParent, wx.Dialog)

    def objShow(self, obj, show=True):
        """objShow is broken out to allow for specialized code"""
        if show=='modal':
            obj.ShowModal()
        else:
            obj.Show(show)
        