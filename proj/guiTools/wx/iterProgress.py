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
from TG.notifications.event import Event

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CanceledException(Exception):
    pass

class IterProgressBasic(object):
    CanceledException = CanceledException
    onUpdate = Event.objProperty()

    def __iter__(self):
        return self

    def close(self):
        pass

    _maximum = None
    def getMaximum(self):
        return self._maximum
    def setMaximum(self, maximum):
        self._maximum = maximum
        
    _label = ""
    def getLabel(self):
        return self._label
    def setLabel(self, label, bUpdate=True):
        self._label = label
        self.update(bUpdate)

    _count = 0
    def getCount(self):
        return self._count
    def setCount(self, count, bUpdate=True):
        self._count = count
        self.update(bUpdate)

    def get(self):
        return self.getCount(), self.getLabel()
    def set(self, count, label, bUpdate=True):
        self.setCount(count, False)
        self.setLabel(label, bUpdate)

    def next(self, label=None, delta=1, bUpdate=True):
        self.setCount(self.getCount()+delta, False)
        self.setLabel(label or self.getLabel(), bUpdate)

    def update(self, bUpdate=True):
        if not bUpdate:
            return False
        self.onUpdate(self._count, self._label)
        return True

class IterProgressDialog(object):
    CanceledException = CanceledException
    onUpdate = Event.objProperty()

    def __init__(self, title, message, maximum=100, *args, **kw):
        self.setCount(0, False)
        self.setLabel(message, False)

        self._dlg_args = (title, message) + args
        kw['maximum'] = maximum
        self._dlg_kw = kw

    def __del__(self):
        self._setDlg(None)

    def __iter__(self):
        return self

    _dlg = None
    def _getDlg(self, bCreate=True):
        if self._dlg is None and bCreate:
            self._setDlg(wx.ProgressDialog(*self._dlg_args, **self._dlg_kw))
        return self._dlg
    def _setDlg(self, newDlg):
        if self._dlg is newDlg: return

        if self._dlg:
            self._dlg.Close()
            self._dlg.Destroy()
            result = True
        else: 
            result = False

        self._dlg = newDlg
        return result

    def close(self):
        self._setDlg(None)

    def getMaximum(self):
        return self._dlg_kw['maximum']
    def setMaximum(self, maximum):
        self._dlg_kw['maximum'] = maximum
        if self._setDlg(None):
            self.update(True)
        
    _label = ""
    def getLabel(self):
        return self._label
    def setLabel(self, label, bUpdate=True):
        self._label = label
        self.update(bUpdate)

    _count = 0
    def getCount(self):
        return self._count
    def setCount(self, count, bUpdate=True):
        self._count = count
        self.update(bUpdate)

    def get(self):
        return self.getCount(), self.getLabel()
    def set(self, count, label, bUpdate=True):
        self.setCount(count, False)
        self.setLabel(label, bUpdate)

    def next(self, label=None, delta=1, bUpdate=True):
        self.setCount(self.getCount()+delta, False)
        self.setLabel(label or self.getLabel(), bUpdate)

    def update(self, bUpdate=True):
        if not bUpdate:
            return False
        try:
            self.onUpdate(self._count, self._label)
            if not self._getDlg().Update(self._count, self._label):
                raise CanceledException()
            return True
        except wx.PyAssertionError, e:
            return False

