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

import wx

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def bitmapFromWindow(window, clientOnly=True):
    '''Code derived from Section `4 Screen Capture`__
    
    .. __: http://wiki.wxpython.org/index.cgi/WorkingWithImages 
    '''

    if clientOnly:
        ctxDC = wx.ClientDC(window)
        w, h = window.GetClientSize()
    else:
        ctxDC = wx.WindowDC(window)
        w, h = window.GetSize()

    bmp = wx.EmptyBitmap(w, h, ctxDC.GetDepth())
    memDC = wx.MemoryDCFromDC(ctxDC)
    memDC.SelectObject(bmp) 
    memDC.Blit(0,0,w,h, ctxDC, 0,0) 
    memDC.SelectObject(wx.NullBitmap) 
    return bmp

