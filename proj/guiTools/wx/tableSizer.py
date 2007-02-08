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

from wx.lib.rcsizer import RowColSizer as TableSizerBase

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TableSizer(TableSizerBase):
    def __init__(self, defaultcellsize=None):
        TableSizerBase.__init__(self)
        self._calcRowsDirty = True
        self._growableRows = []
        self._growableRowsRange = None
        self._calcColsDirty = True
        self._growableCols = []
        self._growableColsRange = None
        if defaultcellsize is not None:
            self.SetDefaultCellSize()

    def SetDefaultCellSize(self, defaultcellsize=(TableSizerBase.col_w, TableSizerBase.row_h)):
        self.col_w, self.row_h = defaultcellsize

    def AddGrowableRow(self, *indicies):
        self._calcRowsDirty = True
        self._growableRows.extend(indicies)

    def SetGrowableRowRange(self, start=None, end=None):
        self._calcRowsDirty = True
        self._growableRowsRange = slice(start, end)

    def AddGrowableCol(self, *indicies):
        self._calcColsDirty = True
        self._growableCols.extend(indicies)

    def SetGrowableColRange(self, start=None, end=None):
        self._calcColsDirty = True
        self._growableColsRange = slice(start, end)

    def RecalcSizes(self):
        if self._calcRowsDirty:
            self.growableRows = self._calculateGrowableRows()
            self._calcRowsDirty = False

        if self._calcColsDirty:
            self.growableCols = self._calculateGrowableCols()
            self._calcColsDirty = False
        return TableSizerBase.RecalcSizes(self)
    
    def _calculateGrowableRows(self):
        try: 
            indexmap = range(len(self.rowHeights))
        except AttributeError: 
            return []

        result = {}
        rowsslice = self._growableRowsRange
        if rowsslice is not None:
            if rowsslice.start is not None: 
                start = rowsslice.start
            else: start = 0
            if rowsslice.stop is not None: 
                stop = rowsslice.stop
            else: stop = len(indexmap)
            for idx in indexmap[start:stop]:
                result[indexmap[idx]] = None

        for idx in self._growableRows:
            result[indexmap[idx]] = None
        result = result.keys()
        result.sort()
        return result

    def _calculateGrowableCols(self):
        try: indexmap = range(len(self.colWidths))
        except AttributeError: return []
        result = {}

        colsslice = self._growableColsRange
        if colsslice is not None:
            if colsslice.start is not None: 
                start = colsslice.start
            else: start = 0
            if colsslice.stop is not None: 
                stop = colsslice.stop
            else: stop = len(indexmap)
            for idx in indexmap[start:stop]:
                result[indexmap[idx]] = None
        for idx in self._growableCols:
            result[indexmap[idx]] = None
        result = result.keys()
        result.sort()
        return result

