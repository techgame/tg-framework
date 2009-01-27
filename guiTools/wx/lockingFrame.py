#!/usr/bin/env python
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##~ Copyright (C) 2002-2004  TechGame Networks, LLC.
##~ 
##~ This library is free software; you can redistribute it and/or
##~ modify it under the terms of the BSD style License as found in the 
##~ LICENSE file included with this distribution.
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""Frame locking (docking) code.

Frame locking (docking) is most useful when there are a LOT of windows about
and our human instincts plead for us to align them."""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import weakref
import wx
from TG.common.bindCallable import weakBindCallable

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class LockSide:
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


    LockingStyles = {
        'standard': (10, 10, 10),
        'attractive': (20, 0, 10),
        'resistive': (0, 20, 10),
        }
    _DeltaAttract, _DeltaResist, _DeltaWing = LockingStyles['standard']

    _LockingSides = [
        ({}, 2), # left - outer
        ({}, 3), # top - outer
        ({}, 0), # right - outer
        ({}, 1), # bottom - outer

        ({}, 0), # left - inner
        ({}, 1), # top - inner
        ({}, 2), # right - inner
        ({}, 3), # bottom - inner
        ]

    Constants = {
        'left': 0, 'top': 1, 'right': 2, 'bottom': 3,
        'innerLeft': 4, 'innerTop': 5, 'innerRight': 6, 'innerBottom': 7,
        'centerHorizontal': 8, 'centerVertical': 9
    }
    locals().update(Constants)
    Constants.update({
        'l': 0, 't': 1, 'r': 2, 'b': 3,
        'il': 4, 'it': 5, 'ir': 6, 'ib': 7,

        # inner
        'inLeft': 4, 'inTop': 5, 'inRight': 6, 'inBottom': 7,
        'inleft': 4, 'intop': 5, 'inright': 6, 'inbottom': 7,

        'iLeft': 4, 'iTop': 5, 'iRight': 6, 'iBottom': 7,
        'ileft': 4, 'itop': 5, 'iright': 6, 'ibottom': 7,

        # center
        'ch': 8, 'cv': 9,
        'cHoriz': 8, 'cVert': 9,
        'cHorizontal': 8, 'cVertical': 9,
    })

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ klass Methods
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def setLockingStyle(self, key='standard'):
        if isinstance(key, tuple): 
            values = key
        else: 
            values = self.LockingStyles[key]
        self._DeltaAttract, self._DeltaResist, self._DeltaWing = values

    def removeSidePositions(self, key):
        for each in self._LockingSides:
            del each[0][key]

    def saveSidePositions(self, key, rect):
        return self.saveSidePositionsEx(key, rect, outsides=True, insides=True, deltas=(self._DeltaAttract, self._DeltaResist, self._DeltaWing))

    def saveSidePositionsEx(klass, key, rect, outsides=True, insides=True, deltas=None):
        l,t,w,h = rect
        dAttract, dResist, dWing = deltas or (klass._DeltaAttract, klass._DeltaResist, klass._DeltaWing)
        if outsides:
            klass._LockingSides[klass.left][0][key] = [(l-dAttract, t, l+dResist, t+h, l)]
            klass._LockingSides[klass.right][0][key] = [(l+w-dResist, t, l+w+dAttract, t+h, l+w)]
            klass._LockingSides[klass.bottom][0][key] = [(l, t+h-dResist, l+w, t+h+dAttract, t+h)]
            klass._LockingSides[klass.top][0][key] = [(l, t-dAttract, l+w, t+dResist, t)]

        if insides:
            klass._LockingSides[klass.innerLeft][0][key] = [(l-dResist, t-dWing, l+dAttract, t, l), (l-dResist, t+h, l+dAttract, t+h+dWing, l)]
            klass._LockingSides[klass.innerRight][0][key] = [(l+w-dAttract, t-dWing, l+w+dResist, t, l+w), (l+w-dAttract, t+h, l+w+dResist, t+h+dWing, l+w)]
            klass._LockingSides[klass.innerBottom][0][key] = [(l-dWing, t+h-dAttract, l, t+h+dResist, t+h), (l+w, t+h-dAttract, l+w+dWing, t+h+dResist, t+h)]
            klass._LockingSides[klass.innerTop][0][key] = [(l-dWing, t-dResist, l, t+dAttract, t), (l+w, t-dResist, l+w+dWing, t+dAttract, t)]
    saveSidePositionsEx = classmethod(saveSidePositionsEx)

    def setupInternalLockingSides(klass, key, rect, deltas=None):
        l,t,w,h = rect
        dAttract, dResist, dWing = deltas or (klass._DeltaAttract, klass._DeltaResist, klass._DeltaWing)
        klass._LockingSides[klass.innerLeft][0][key] = [(l-dResist, t, l+dAttract, t+h, l)]
        klass._LockingSides[klass.innerRight][0][key] = [(l+w-dAttract, t, l+w+dResist, t+h, l+w)]
        klass._LockingSides[klass.innerBottom][0][key] = [(l, t+h-dAttract, l+w, t+h+dResist, t+h)]
        klass._LockingSides[klass.innerTop][0][key] = [(l, t-dResist, l+w, t+dAttract, t)]
    setupInternalLockingSides = classmethod(setupInternalLockingSides)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class LockingFrameMixin(LockSide):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    _weakself = None
    __bLocking = 0

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __init__(self, *args, **kw):
        wx.EVT_SIZE(self, weakBindCallable(self._onSizeFrame))
        wx.EVT_MOVE(self, weakBindCallable(self._onMoveFrame))
        self.PushEventHandler(wx.EvtHandler())

    def Show(self, bShow=1):
        result = self.mixinKlass.Show(self, bShow)
        self._saveSidePositions()
        return result

    def Move(self, pos):
        self.__bLocking = 1
        if isinstance(pos, (tuple, list)): newpos = pos
        else: newpos = pos.x, pos.y

        newpos, newsize = self._onLockingMove(newpos, tuple(self.GetSize())) or newpos
        result = self.mixinKlass.Move(self, newpos)

        self.__bLocking = 0
        return result

    def SetDimensions(self, x, y, w, h, *args, **kw):
        self.__bLocking= 1
        newpos, newsize = self._onLockingMove((x,y), (w,h))
        newpos, newsize = self._onLockingSize(newpos, newsize)
        result = self._doSetDimensions(*(newpos + newsize + args), **kw)
        self.__bLocking= 0
        return result

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def lockToSelf(self, frame, lockSideIndicies=(LockSide.bottom,LockSide.innerLeft), lockSizeIndicies=()):
        return lockWindowsTogether(self, frame, lockSideIndicies, lockSizeIndicies)
    lockFrameToSelf = lockToSelf

    def lockTo(self, frame, lockSideIndicies=(LockSide.bottom,LockSide.innerLeft), lockSizeIndicies=()):
        return lockWindowsTogether(frame, self, lockSideIndicies, lockSizeIndicies)
    lockToFrame = lockTo

    def lockToDesktop(self, lockSideIndicies=(LockSide.innerTop,LockSide.innerLeft), lockSizeIndicies=()):
        return lockToDesktop(self, lockSideIndicies, lockSizeIndicies)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Event Handlers
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _onSizeFrame(self, evt):
        if not self.__bLocking:
            self.__bLocking = 1
            pos, size = tuple(self.GetPosition()), tuple(self.GetSize())
            newpos, newsize = self._onLockingSize(pos, size)
            self._doSetDimensions(*(newpos + newsize))
            self.__bLocking = 0
        self._saveSidePositions()
        evt.Skip()

    def _onMoveFrame(self, evt):
        if not self.__bLocking:
            self.__bLocking= 1
            pos, size = tuple(self.GetPosition()), tuple(self.GetSize())
            newpos, newsize = self._onLockingMove(pos, size)
            self._doSetDimensions(*(newpos + newsize))
            self.__bLocking= 0
        self._saveSidePositions()
        evt.Skip()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Protected Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _doSetDimensions(self, *args, **kw):
        self.mixinKlass.SetDimensions(self, *args, **kw)

    def _removeSidePositions(self):
        if self._weakself:
            self.removeSidePositions(self._weakself)
            self._weakself = None

    def _saveSidePositions(self):
        if not self.IsShown() or self.IsIconized():
            return self._removeSidePositions()
        self._weakself = weakref.ref(self)
        l,t,w,h = self.GetRect()
        self.saveSidePositions(self._weakself, (l,t,w,h))

    def _onLockingMove(self, pos, size):
        (l,t),(w,h) = pos, size
        IntersectionSides = _getIntersectionSides(l,t,w,h)
        for (LockingSides, WidthIdx), FrameSide in zip(self._LockingSides, IntersectionSides):
            for weakframe, SideList in LockingSides.iteritems():
                if weakframe is self._weakself: continue
                for Side in SideList:
                    if _intersects(FrameSide, Side):
                        if WidthIdx == 0: pos = Side[-1], pos[1], 
                        elif WidthIdx == 1: pos = pos[0], Side[-1], 
                        elif WidthIdx == 2: pos = Side[-1]-w, pos[1], 
                        elif WidthIdx == 3: pos = pos[0], Side[-1]-h, 
                        break
        return pos, size

    def _onLockingSize(self, pos, size):
        (l,t),(w,h) = pos, size
        IntersectionSides = _getIntersectionSides(l,t,w,h)
        for (LockingSides, WidthIdx), FrameSide in zip(self._LockingSides, IntersectionSides):
            for weakframe, SideList in LockingSides.iteritems():
                if weakframe is self._weakself: continue
                for Side in SideList:
                    if _intersects(FrameSide, Side):
                        if WidthIdx == 0: pos = Side[-1], pos[1], 
                        elif WidthIdx == 1: pos = pos[0], Side[-1], 
                        elif WidthIdx == 2: size = Side[-1]-pos[0], size[1], 
                        elif WidthIdx == 3: size = size[0], Side[-1]-pos[1], 
                        break
        return pos, size

    def mixedWith(klass, mixFrame):
        try:
            return klass.__mixResults[mixFrame]
        except AttributeError: klass.__mixResults = {}
        except LookupError: pass

        class LockingFrameBase(klass, mixFrame): 
            mixinKlass = mixFrame
            def __init__(self, *args, **kw):
                mixFrame.__init__(self, *args, **kw)
                klass.__init__(self, *args, **kw)
        LockingFrameBase.__name__ = 'Locking'+mixFrame.__name__

        klass.__mixResults[mixFrame] = LockingFrameBase
        return LockingFrameBase
    mixedWith = classmethod(mixedWith)
LockingFrameMixin.setupInternalLockingSides(None, tuple(wx.GetClientDisplayRect()))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

LockingFrame = LockingFrameMixin.mixedWith(wx.Frame)
LockingMiniFrame = LockingFrameMixin.mixedWith(wx.MiniFrame)
LockingMDIParentFrame = LockingFrameMixin.mixedWith(wx.MDIParentFrame)
LockingMDIChildFrame = LockingFrameMixin.mixedWith(wx.MDIChildFrame)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Utilities 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def lockWindowsTogether(HostWin, AttachWin, lockSideIndicies=(LockSide.bottom,LockSide.innerLeft), lockSizeIndicies=()):
    if HostWin.IsTopLevel() ^ AttachWin.IsTopLevel():
        # If both HostWin xor AttachWin are top level windows (Frame or Dialog), then figure out screen coordinates
        hostrect = tuple(HostWin.ClientToScreen((0,0))) + tuple(HostWin.GetSize())
    else:
        # Otherwise, assume that they are in the same frame of reference.  (Until we get a bug for shortsightedness ;)
        hostrect = tuple(HostWin.GetRect())
    positions = tuple(_getIntersectionPositions(hostrect, AttachWin.GetSize()))
    lockSideValues, lockSizeValues = _translateLockValues(lockSideIndicies, lockSizeIndicies, positions)
    return _doLockWindowToPositon(AttachWin, lockSideValues, lockSizeValues)

def lockToDesktop(AttachWin, lockSideIndicies=(LockSide.innerTop,LockSide.innerLeft), lockSizeIndicies=()):
    positions = tuple(_getIntersectionPositions(wx.GetClientDisplayRect(), AttachWin.GetSize()))
    lockSideValues, lockSizeValues = _translateLockValues(lockSideIndicies, lockSizeIndicies, positions)
    return _doLockWindowToPositon(AttachWin, lockSideValues, lockSizeValues)

def _getLockValue(key):
    if key in LockSide.Constants:
        return LockSide.Constants[key]
    else: return int(key)

def _translateLockValues(lockSideIndicies, lockSizeIndicies, positions):
    if isinstance(lockSideIndicies, basestring):
        lockSideIndicies = filter(None, [s.strip() for s in lockSideIndicies.split(',')])
        lockSideIndicies = map(_getLockValue, lockSideIndicies)
    lockSideIndicies = map(positions.__getitem__, lockSideIndicies)

    if isinstance(lockSizeIndicies, basestring):
        lockSizeIndicies = filter(None, [s.strip() for s in lockSizeIndicies.split(',')])
        lockSizeIndicies = map(_getLockValue, lockSizeIndicies)
    lockSizeIndicies = map(positions.__getitem__, lockSizeIndicies)

    # Lookup the constant aliases
    return lockSideIndicies, lockSizeIndicies

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def _doLockWindowToPositon(window, lockSideValues, lockSizeValues, pos=None, size=None):
    pos, size = pos or tuple(window.GetPosition()), size or tuple(window.GetSize())
    for lockpos in lockSideValues:
        if lockpos[0] is None:
            pos = pos[0], lockpos[1]
        else:
            pos = lockpos[0], pos[1]

    newpos, pos = pos, (pos[0] + size[0], pos[1] + size[1])
    for lockpos in lockSizeValues:
        if lockpos[0] is None:
            pos = pos[0], lockpos[1]
        else:
            pos = lockpos[0], pos[1]

    newsize = abs(pos[0] - newpos[0]), abs(pos[1] - newpos[1])
    newpos = tuple(map(min, zip(pos, newpos)))

    window.SetDimensions(*(newpos + newsize))
    return window

def _getIntersectionPositions((l, t, w, h), (wP, hP)=(0,0)):
    return [
        (l, None), #leftSide
        (None, t), #topSide
        (l+w, None), #rightSide
        (None, t+h), #bottomSide

        (l, None), #innerLeft
        (None, t), #innerTop
        (l+w-wP, None), #innerRight
        (None, t+h-hP), #innerBottom

        (l+(w-wP)/2, None), #centerHorizontal
        (None, t+(h-hP)/2), #centerVertical
        ]

def _getIntersectionSides(l, t, w, h):
    return [
        (l+w, t, l+w, t+h), # right - outter
        (l, t+h, l+w, t+h), # bottom - outter
        (l, t, l, t+h), # left - outter
        (l, t, l+w, t), # top - outter

        (l, t, l, t+h), # left - inner
        (l, t, l+w, t), # top - inner
        (l+w, t, l+w, t+h), # right - inner
        (l, t+h, l+w, t+h), # bottom - inner
        ]

def _intersects(A, B):
    if A[0] > B[2]: return 0
    if B[0] > A[2]: return 0
    if A[1] > B[3]: return 0
    if B[1] > A[3]: return 0
    return 1

