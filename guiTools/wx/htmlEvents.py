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
import wx.html

from TG.guiTools.wx import wxVersion, wxClasses

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ wxVersion Adaptation
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Ugly adaption for wx-2.4 vs wx-2.5 event changes
if wxVersion() >= "2.5":
    _eventBinder = wx.PyEventBinder
else:
    def _eventBinder(EventType, numIds=1):
        assert numIds == 1
        def dynamic_EVT(win, id, func):
            win.Connect(id, -1, EventType, func)
        return dynamic_EVT

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Event Clasess
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class HtmlWindowEvent(wx.PyCommandEvent):
    EventType = None

    def __init__(self, eventObject):
        wx.PyCommandEvent.__init__(self, self.EventType, eventObject.GetId())
        self.SetEventObject(eventObject)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class HtmlWindow_LinkClickedEvent(HtmlWindowEvent):
    EventType = wx.NewEventType()

    link = None
    def GetLink(self):
        return self.link
    def SetLink(self, link):
        self.link = link

EVT_HTMLWIN_LINK = _eventBinder(HtmlWindow_LinkClickedEvent.EventType, 1)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class HtmlWindow_SetTitleEvent(HtmlWindowEvent):
    EventType = wx.NewEventType()

    title = None
    def GetTitle(self):
        return self.title
    def SetTitle(self, title):
        self.title = title

EVT_HTMLWIN_SETTITLE = _eventBinder(HtmlWindow_SetTitleEvent.EventType, 1)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class HtmlWindow_CellEvent(HtmlWindowEvent):
    cell = None
    def GetCell(self):
        return self.cellwx.NewEventType()
    def SetCell(self, cell):
        self.cell = cell

    position = None
    def GetPosition(self):
        return self.position
    def SetPosition(self, position):
        self.position = position

    mouseEvent = None
    def GetMouseEvent(self):
        return self.mouseEvent
    def SetMouseEvent(self, mouseEvent):
        self.mouseEvent = mouseEvent


class HtmlWindow_CellHoverEvent(HtmlWindow_CellEvent):
    EventType = wx.NewEventType()
EVT_HTMLWIN_CELL_HOVER = _eventBinder(HtmlWindow_CellHoverEvent.EventType, 1)

class HtmlWindow_CellClickedEvent(HtmlWindow_CellEvent):
    EventType = wx.NewEventType()
EVT_HTMLWIN_CELL_CLICKED = _eventBinder(HtmlWindow_CellClickedEvent.EventType, 1)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ HtmlWindow that fires events instead of virtual methods
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class HtmlWindowWithEvents(wx.html.HtmlWindow):
    def OnLinkClicked(self, link):
        evt = HtmlWindow_LinkClickedEvent(self)
        evt.SetLink(link)

        runBase = not self.ProcessEvent(evt)
        runBase = runBase or evt.GetSkipped()
        if runBase:
            return self.base_OnLinkClicked(link)

    def OnSetTitle(self, title):
        evt = HtmlWindow_SetTitleEvent(self)
        evt.SetTitle(title)

        runBase = not self.ProcessEvent(evt)
        runBase = runBase or evt.GetSkipped()
        if runBase:
            return self.base_OnSetTitle(title)

    def OnCellMouseHover(self, cell, x, y):
        evt = HtmlWindow_CellHoverEvent(self)
        evt.SetCell(cell)
        evt.SetPosition((x,y))

        runBase = not self.ProcessEvent(evt)
        runBase = runBase or evt.GetSkipped()
        if runBase:
            return self.base_OnCellMouseHover(cell, x, y)

    def OnCellClicked(self, cell, x, y, event):
        evt = HtmlWindow_CellClickedEvent(self)
        evt.SetCell(cell)
        evt.SetPosition((x,y))
        evt.SetMouseEvent(event)

        runBase = not self.ProcessEvent(evt)
        runBase = runBase or evt.GetSkipped()
        if runBase:
            return self.base_OnCellClicked(cell, x, y, event)

