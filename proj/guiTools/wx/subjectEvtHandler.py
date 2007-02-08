#!/usr/bin/env python
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##~ Copyright (C) 2002-2004  TechGame Networks, LLC.
##~ 
##~ This library is free software; you can redistribute it and/or
##~ modify it under the terms of the BSD style License as found in the 
##~ LICENSE file included with this distribution.
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""A subject/observer implementation of a EvtHandler"""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import wx

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class EventSubject(object):
    def __init__(self):
        self.observers = []

    def Connect(self, function, *args):
        self.observers.insert(0, (function, args))

    def Disconnect(self, function, *args):
        self.observers = [x for x in self.observers if x[0] != function]

    def Notify(self, evt, *args):
        result = NotImplemented
        for observer, obsargs in self.observers:
            if evt.GetSkipped():
                # Restore it to not skipped
                evt.Skip(False)
            result = observer(evt, *(args+obsargs))

        if result is NotImplemented:
            evt.Skip()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SubjectEvtHandler(wx.EvtHandler):
    def forEvtHandler(klass, evtHandler):
        try:
            if evtHandler.__setup:
                return evtHandler
        except AttributeError: 
            result = klass()
            result.replaceEvtHandlerOf(evtHandler)
        return result
    forEvtHandler = classmethod(forEvtHandler)

    def replaceEvtHandlerOf(self, evtHandler):
        evtHandler.SetNextHandler(self)
        self.SetPreviousHandler(evtHandler)
        evtHandler.__setup = True

    def Connect(self, id, lastid, eventType, function, *args, **kw):
        if lastid < 0: wxidrange = (id,)
        else: wxidrange = range(id, lastid)

        # Iterate through the id range manually
        for wxid in wxidrange:
            key = (wxid, -1, eventType)
            try: subject = self.subjectMap[key]
            except KeyError:
                subject = EventSubject()
                self.subjectMap[key] = subject
                # Connect the subject to the event
                subjectargs = key + (subject.Notify,)
                wx.EvtHandler.Connect(self, *subjectargs)

            #connect the function to the subject
            subject.Connect(function, *args, **kw)

    def Disconnect(self, id, lastid, eventType, function, *args):
        if lastid < 0: wxidrange = (id,)
        else: wxidrange = range(id, lastid)

        # Iterate through the id range manually
        for wxid in wxidrange:
            key = (wxid, -1, eventType)
            try: subject = self.subjectMap[key]
            except KeyError: pass
            else: subject.Disconnect(function, *args)

    def _getSubjectMap(self):
        try: 
            return self._subject_map
        except AttributeError:
            self._subject_map = {}
            return self._subject_map
    subjectMap = property(_getSubjectMap)

