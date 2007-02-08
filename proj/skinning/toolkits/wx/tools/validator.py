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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SkinValidator(wx.PyValidator):
    host = None

    def __init__(self, host, **kw):
        wx.PyValidator.__init__(self)

        self.host = host

        kw.pop('this', None)
        kw.pop('thisown', None)
        self.__dict__.update(kw)

    def Clone(self):
        return self.__class__(**vars(self))

    def Validate(self, window):
        if self.host is not None:
            return self.host._onValidate(window)
        else:
            return True

    def TransferToWindow(self):
        return True
    def TransferFromWindow(self):
        return True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

validateCodeTemplate = """def _validate(window, %s, **kw): %s
pyelem.setValidateCallback(_validate)
"""

class validator(wxPyWidgetBaseSkinElement):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    codeTemplate = validateCodeTemplate
    validateCallback = None

    defaultSettings = wxPyWidgetBaseSkinElement.defaultSettings.copy()
    defaultSettings.update({ 
        })

    defaultStyleSettings = wxPyWidgetBaseSkinElement.defaultStyleSettings.copy()
    defaultStyleSettings.update({
        })

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Definitions 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def createWidget(self, parentObj):
        parentObj.SetValidator(SkinValidator(self))
        # You must get the validator from parentObj because
        # SetValidator calls Clone()
        obj = parentObj.GetValidator() 
        return obj

    def finishWidget(self, obj, parentObj):
        pass

    def installDefaultEvent(self, evtHandler, evtObject, evtCallback):
        wx.EVT_CHAR(evtHandler, evtCallback)

    def getValidateCallback(self):
        return self.validateCallback
    def setValidateCallback(self, validateCallback):
        self.validateCallback = validateCallback
    def _onValidate(self, window):
        return self.getValidateCallback()(**self.getLocals(window=window))
    def _applyCodeTemplate(self, content):
        # to handle the parameter names for the function
        paramNames = ', '.join(self.getLocals().keys())
        return self.codeTemplate % (paramNames, content,)

    def getEvtObject(self):
        return self.getParentObj()
    def getExecModule(self):
        return self.xmlParent().getExecModule()
    def getGlobals(self):
        return self.xmlParent().getGlobals()
    def refreshLocals(self, elementLocals):
        elementLocals.update({
            'pyelem':self, 
            'validator':self.getObject(),

            'elem':self.xmlParent(), 
            'ctx':self.getContext(),
            'obj':self.getEvtObject(),
            })
