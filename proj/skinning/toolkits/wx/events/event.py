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

from TG.skinning.toolkits.wx._baseElements import *
from TG.guiTools.wx.subjectEvtHandler import SubjectEvtHandler

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

eventCodeTemplate = """def _event(evt, %s, **kw): %s 
pyelem.setEvtCallback(_event)
"""

class EventMixin:
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    codeTemplate = eventCodeTemplate
    evtCallback = None
    evtHandlerTypes = wxClasses(wx.EvtHandler)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Definitions 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def hookEvent(self):
        return self.installEvent(self.getEvtHandler(), self.getEvtObject(), self._onEvent)
    def installEvent(self, evtHandler, evtObject, evtCallback):
        return self.installDefaultEvent(evtHandler, evtObject, evtCallback)
    def installDefaultEvent(self, evtHandler, evtObject, evtCallback):
        raise NotImplementedError

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getEvtHandler(self):
        evtHandler = self.getEvtObject()
        if isinstance(evtHandler, self.evtHandlerTypes):
            return evtHandler
        else:
            return None
    def getEvtObject(self):
        return self.getObject()
    def getEvtCallback(self):
        return self.evtCallback
    def setEvtCallback(self, evtCallback):
        self.evtCallback = evtCallback

    def _findEvtCallback(self):
        evtCallback = self.getEvtCallback()
        if evtCallback is None:
            code = self.compile(self.getSetting('run', 'None'), 'eval')
            def evtCallback(evt, elem, obj, ctx, code=code, **kw):
                return self.evaluate(code, evt=evt, elem=elem, obj=obj, ctx=ctx, **kw)
            self.setEvtCallback(evtCallback)
        return evtCallback

    def _onEvent(self, evt):
        onEvent = self._findEvtCallback()
        skinLocals = self.getLocals(evt=evt)
        return onEvent(**skinLocals)

    def _applyCodeTemplate(self, content):
        # to handle the parameter names for the function
        paramNames = ', '.join(self.getLocals().keys())
        return self.codeTemplate % (paramNames, content,)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class event(EventMixin, wxPySkinElement):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    defaultSettings = wxPySkinElement.defaultSettings.copy()
    defaultSettings.update({ 
        })

    defaultStyleSettings = wxPySkinElement.defaultStyleSettings.copy()
    defaultStyleSettings.update({
        'wxid': 'None',
        'wxid-end': 'None',
        'enabled': 'True', 
        })

    objParentTypes = EventMixin.evtHandlerTypes
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Definitions 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def xmlPreAddElement(self, elemBuilder, name, attributes, srcref):
        # TODO: Replace with exception that actually redirects to the source file
        raise Exception('"%s" element cannot have any child elements! %r %r' % (self.__class__.__name__, name, attributes))

    def xmlInitStarted(self, elemBuilder):
        self.initialStandardOptions()
        return wxPySkinElement.xmlInitStarted(self, elemBuilder)

    def xmlInitFinalized(self, elemBuilder):
        wxPySkinElement.xmlInitFinalized(self, elemBuilder)
        if self.getStyleSettingEval('enabled', True):
            self.hookEvent()
        self.finalStandardOptions()

    def getEvtCallback(self):
        return self.getObject()
    def setEvtCallback(self, evtCallback):
        self.setObject(evtCallback)

    def getEvtHostObject(self):
        try: 
            self.xmlParent().getEvtHostObject
        except AttributeError:
            return self.getEvtObject()
        else:
            return self.xmlParent().getEvtHostObject()
    def getEvtObject(self):
        parent = self.xmlParent()
        if parent is not None:
            try: 
                parent.getEvtObject
            except AttributeError:
                result = parent.getObject()
            else:
                result = parent.getEvtObject()
        else:
            result = None
        return result

    def getEvtHandler(self):
        try: 
            self.xmlParent().getEvtHandler
        except AttributeError:
            # try base class approach
            return EventMixin.getEvtHandler(self)
        else:
            evtHandler = self.xmlParent().getEvtHandler()
            if isinstance(evtHandler, self.evtHandlerTypes):
                evtHandler = SubjectEvtHandler.forEvtHandler(evtHandler)
            return evtHandler

    def installEvent(self, evtHandler, evtObject, evtCallback):
        if not evtHandler:
            return None

        if self.hasSetting('type'):
            evtType = self.getSettingEval('type')
            return self.installEventForType(evtType, evtHandler, evtObject, evtCallback)
        else:
            return self.installDefaultEvent(evtHandler, evtObject, evtCallback)

    def installDefaultEvent(self, evtHandler, evtObject, evtCallback):
        install = getattr(self.xmlParent(), 'installDefaultEvent', None)
        if install is not None:
            return install(evtHandler, evtObject, evtCallback)

    if wxVersion() < '2.5':
        # wx-2.4 event code

        def getEventId(self, evtObject):
            wxid = self.getStyleSettingEval('wxid')
            if wxid is None:
                wxid = evtObject.GetId()
            return wxid

        def installEventForType(self, evtType, evtHandler, evtObject, evtCallback):
            try:
                return evtType(evtHandler, evtCallback)
            except (AssertionError, TypeError):
                return evtType(evtHandler, self.getEventId(evtObject), evtCallback)
    else:
        # wx-2.5 event code

        def getEventBindKW(self, evtObject, **kw):
            wxid = self.getStyleSettingEval('wxid')
            if wxid is not None:
                kw['id'] = wxid

            wxidEnd = self.getStyleSettingEval('wxid-end')
            if wxidEnd is not None:
                kw['id2'] = wxidEnd

            return kw

        def installEventForType(self, evtType, evtHandler, evtObject, evtCallback):
            kwBind = self.getEventBindKW(evtObject)
            if evtType.expectedIDs:
                return evtHandler.Bind(evtType, evtCallback, evtObject, **kwBind)
            else:
                return evtHandler.Bind(evtType, evtCallback, **kwBind)

    def getExecModule(self):
        parent = self.xmlParent()
        if parent is not None:
            return parent.getExecModule()
    def getGlobals(self):
        parent = self.xmlParent()
        if parent is not None:
            return parent.getGlobals()
    def refreshLocals(self, elementLocals):
        elementLocals.update({
            'pyelem':self, 
            'elem':self.xmlParent(), 
            'ctx':self.getContext(),
            'obj':self.getEvtHostObject(),
            })
