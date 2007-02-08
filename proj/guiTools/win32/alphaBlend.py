#!/usr/bin/env python
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##~ Copyright (C) 2002-2004  TechGame Networks, LLC.
##~ 
##~ This library is free software; you can redistribute it and/or
##~ modify it under the terms of the BSD style License as found in the 
##~ LICENSE file included with this distribution.
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""Microsoft Windows specific calls for Alpha Blending windows.

Dependent upon ctypes.
"""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import ctypes

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Constants / Variables / Etc. 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

GWL_EXSTYLE = 0xffffffec
WS_EX_LAYERED = 0x00080000
LWA_COLORKEY = 0x00000001
LWA_ALPHA = 0x00000002
user32 = ctypes.windll.user32

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class AlphaBlendBase(object):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    alpha = 1.0
    colorkey = None
    hWnd = 0

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def SetHandle(self, hWnd): 
        if isinstance(hWnd, (int, long)):
            self.hWnd = hWnd
        elif hWnd is None:
            self.hWnd = hWnd
        else:
            self.hWnd = hWnd.GetHandle()

    def GetHandle(self): 
        return self.hWnd

    def isAlphaBlendingEnabled(self):
        hWnd = self.GetHandle()
        if hWnd is not None:
            style = user32.GetWindowLongA(hWnd, GWL_EXSTYLE)
            return bool(style & WS_EX_LAYERED)
        else:
            return False

    def enableAlphaBlending(self, enable=True):
        hWnd = self.GetHandle()
        if hWnd is not None:
            style = user32.GetWindowLongA(hWnd, GWL_EXSTYLE)
            if enable: style |= WS_EX_LAYERED
            else: style &= ~WS_EX_LAYERED
            user32.SetWindowLongA(hWnd, GWL_EXSTYLE, style)
            return True
        else: 
            return False

    def AlphaBlend(self, alpha=None, colorkey=None, usedefaults=True):
        hWnd = self.GetHandle()
        if hWnd is None: 
            raise ValueError("Handle must be valid before calling AlphaBlend")

        flag = 0
        if alpha is not None:
            self.alpha = alpha
            alpha = int(255 * alpha)
            flag |= LWA_ALPHA
        elif usedefaults: 
            alpha = int(255 * self.alpha)
            if alpha < 255: flag |= LWA_ALPHA
        else: 
            self.alpha = 1.0
            alpha = 255

        if colorkey is not None:
            flag |= LWA_COLORKEY
            self.colorkey = colorkey
        elif usedefaults: 
            if self.colorkey is None: 
                colorkey = 0
            else: 
                colorkey = self.colorkey
                if colorkey is not None:
                    flag |= LWA_COLORKEY
        else:
            colorkey = 0
            self.colorkey = None

        user32.SetLayeredWindowAttributes(hWnd, colorkey, alpha, flag)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class winAlphaBlend(AlphaBlendBase):
    def __init__(self, hWnd=None, enable=True):
        self.SetHandle(hWnd)
        self.enableAlphaBlending(enable)

