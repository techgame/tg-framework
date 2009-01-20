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

import wx

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ListColumnWidthSizerMixin:
    """Size the columns of the list control in the same fashion that as sizers
    are used for laying out windows.
    
    Inspired by wx.lib.mixins.listctrl.ListCtrlAutoWidthMixin"""

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Imports 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    _absWidths = None
    _relWidths = None

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getAbsColumnWidths(self):
        if self._absWidths is None:
            self._absWidths = []
        if self:
            neededColumns = [self.GetColumnWidth(idx) for idx in range(len(self._absWidths), self.GetColumnCount())]
            if neededColumns:
                self._absWidths.extend(neededColumns)
        return self._absWidths
    def setAbsColumnWidths(self, widths):
        self._absWidths = list(widths)
    def setAbsColumnWidth(self, column, width):
        self.getAbsColumnWidths()[column] = width

    def getRelColumnWidths(self):
        if self._relWidths is None:
            self._relWidths = []
        if self:
            neededColumns = [0 for idx in range(len(self._relWidths), self.GetColumnCount())]
            if neededColumns:
                self._relWidths.extend(neededColumns)
        neededColumns = max(0, self.GetColumnCount()-len(self._relWidths))
        if neededColumns:
            self._relWidths.extend([0] * neededColumns)
        return self._relWidths
    def setRelColumnWidths(self, widths):
        self._relWidths = list(widths)
    def setRelColumnWidth(self, column, width):
        self.getRelColumnWidths()[column] = width

    def getColumnWidths(self):
        return zip(self.getRelColumnWidths(), self.getAbsColumnWidths())
    def setColumnWidths(self, widths):
        widths = zip(*[self._getWidthsFromValue(w) for w in widths])
        self.setRelColumnWidths(widths[0])
        self.setAbsColumnWidths(widths[1])

    def setColumnWidth(self, column, value):
        relW, absW = self._getWidthsFromValue(value)
        self.setRelColumnWidth(column, relW)
        self.setAbsColumnWidth(column, absW)

    def _getWidthsFromValue(self, value):
        if isinstance(value, tuple):
            if len(value) == 1:
                return value[0], 0
            else:
                return value[0], int(value[1])
        else:
            return 0, int(value)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _bindColumnSizingEvents(self):
        wx.EVT_SIZE(self, self._onResizeList)
        wx.EVT_LIST_COL_END_DRAG(self, self.GetId(), self._onResizeListColumn)

    def _onResizeListColumn(self, evt):
        evt.Skip()
        wx.CallAfter(self._doResizeListColumnIdx, evt.GetColumn())
    def _doResizeListColumnIdx(self, col):
        # set the min width to the current (re)size of the column, and make
        # sure it is no longer relative
        self.setColumnWidth(col, self.GetColumnWidth(col))
        # redraw the rest of the columns...
        self._doResizeListColumns()

    def _onResizeList(self, evt):
        evt.Skip()
        self._doResizeListColumns()
    def _doResizeListColumns(self):
        # We're showing the vertical scrollbar -> allow for scrollbar width
        # NOTE: on GTK, the scrollbar is included in the client size, but on
        # Windows it is not included
        listWidth = self.GetClientSize().width
        if wx.Platform != '__WXMSW__':
            if self.GetItemCount() > self.GetCountPerPage():
                listWidth -= wx.SystemSettings_GetMetric(wx.SYS_VSCROLL_X)

        numCols = self.GetColumnCount()
        totalAbsWidth = sum(self.getAbsColumnWidths()[:numCols], 0.0)
        remainingWidth = max(0.0, listWidth - totalAbsWidth)
        relativeWeights = max(1.0, sum(self.getRelColumnWidths()[:numCols], 0.0))
        relStep = remainingWidth/relativeWeights

        for idx, (relW, absW) in enumerate(zip(self.getRelColumnWidths(), self.getAbsColumnWidths())[:numCols]):
            self.SetColumnWidth(idx, int(absW + relW*relStep))

