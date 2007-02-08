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

from layout_grid import *

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class layout_grid_flex(layout_grid):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    defaultSettings = layout_grid.defaultSettings.copy()
    defaultSettings.update({ 
        })

    defaultStyleSettings = layout_grid.defaultStyleSettings.copy()
    defaultStyleSettings.update({
        'gap': '(0,0)',
        'grow-rows': '()',
        'grow-cols': '()',
        })

    if wxVersion() >= '2.5':
        defaultStyleSettings.update({
            'direction': 'BOTH',
            'mode': 'FLEX_GROWMODE_SPECIFIED',
            })

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Definitions 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def createWidget(self, parentObj):
        rows = self.getStyleSettingEval('rows')
        cols = self.getStyleSettingEval('cols')
        hgap,vgap = self.getStyleSettingEval('gap')
        obj = wx.FlexGridSizer(rows, cols, vgap, hgap)
        self.setFlexGridSettings(obj)
        self.setGrowableRows(obj, rows)
        self.setGrowableColumns(obj, cols)
        return obj

    def setGrowableRows(self, obj, rows):
        growrows = self.getStyleSettingEval('grow-rows')
        if isinstance(growrows, dict):
            growrows = growrows.items()
        
        for entry in growrows:
            if isinstance(entry, int):
                idx, proportion = entry, 1
            else: idx, proportion = entry

            if idx < 0:
                idx = max(0, rows+idx)
            elif idx >= rows:
                idx = rows-1

            self._addGrowableRow(obj, idx, proportion)

    def setGrowableColumns(self, obj, cols):
        growcols = self.getStyleSettingEval('grow-cols')
        if isinstance(growcols, dict):
            growcols = growcols.items()
        
        for entry in growcols:
            if isinstance(entry, int):
                idx, proportion = entry, 1
            else: idx, proportion = entry

            if idx < 0:
                idx = max(0, cols+idx)
            elif idx >= cols:
                idx = cols-1

            self._addGrowableCol(obj, idx, proportion)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    if wxVersion() < '2.5':
        # no proportion argument in 2.4
        def _addGrowableCol(self, obj, idx, proportion):
            obj.AddGrowableCol(idx)
        # no proportion argument in 2.4
        def _addGrowableRow(self, obj, idx, proportion):
            obj.AddGrowableRow(idx)
        # version 2.4 doesn't have those options
        def setFlexGridSettings(self, obj):
            pass
    else:
        def _addGrowableCol(self, obj, idx, proportion):
            obj.AddGrowableCol(idx, proportion)
        def _addGrowableRow(self, obj, idx, proportion):
            obj.AddGrowableRow(idx, proportion)
        def setFlexGridSettings(self, obj):
            direction = self.getStyleSettingEval('direction')
            obj.SetFlexibleDirection(direction)

            mode = self.getStyleSettingEval('mode')
            obj.SetNonFlexibleGrowMode(mode)

