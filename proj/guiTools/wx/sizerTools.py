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

import weakref

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def getAdjsutedClientSize(parent, layout):
    minSize = tuple(layout.GetMinSize())
    clientSize = tuple(parent.GetClientSize())
    return [max(mS, cS) for mS, cS in zip(minSize, clientSize)]

def getAdjustedSizeHints(parent, layout):
    minSize = tuple(layout.GetMinSize())
    clientSize = tuple(parent.GetClientSize())
    size = tuple(parent.GetSize())

    # adjust the overall size hints to minSize
    return [minS + (S-cS) for minS,S,cS in zip(minSize, size, clientSize)]

def adjustLayoutContainerSizes(parent, layout, virtual=False):
    clientSize = getAdjsutedClientSize(parent, layout)
    parent.SetClientSize(clientSize)

    sizeHints = getAdjustedSizeHints(parent, layout)
    if virtual:
        parent.SetVirtualSizeHints(*sizeHints)
    else:
        parent.SetSizeHints(*sizeHints)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class HostLayoutLink(object):
    _sizer = None
    _sizerItem = None

    def __init__(self, hostSizer, hostSizerItem):
        self.setSizer(hostSizer)
        self.setSizerItem(hostSizerItem)
        
    def forLayoutObj(klass, layoutObj, hostSizer, hostSizerItem):
        if hostSizerItem is None and hasattr(hostSizer, 'GetItem'):
            hostSizerItem = hostSizer.GetItem(layoutObj)
        if hostSizerItem is None or hostSizerItem.IsSpacer():
            return None

        result = klass(hostSizer, hostSizerItem)
        result.addToLayoutObj(layoutObj)
        return result
    forLayoutObj = classmethod(forLayoutObj)

    def addToLayoutObj(self, layoutObj):
        layoutObj.layoutLink = self

    def getSizerItem(self, resolve=True):
        return self._sizerItem
    def setSizerItem(self, hostSizerItem):
        self._sizerItem = hostSizerItem
        
    def getSizer(self, resolve=True):
        result = self._sizer
        if resolve:
            result = result()
        return result
    def setSizer(self, hostSizer):
        try:
            self._sizer = weakref.ref(hostSizer)
        except TypeError:
            self._sizer = lambda: hostSizer

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def Layout(self):
        self.getSizer().Layout()

    def IsShown(self):
        return self.getSizerItem().IsShown()

    def Show(self, bShow=True):
        self.getSizerItem().Show(bShow)
        self.Layout()
        return bShow

    def Hide(self):
        return self.Show(False)

    def ShowToggle(self):
        return self.Show(not self.IsShown())

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

