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

from TG.skinning.common.cssElement import CSSSkinElement
from TG.skinning.engine.xmlSkinner import XMLFactory
import store
import section

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class template(store.ElementRestoreMixin, CSSSkinElement):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    xmlFactories = section.section.xmlFactories

    mode = None
    _StoringMode = 1
    _ExpandingMode = 2
    _InvokingMode = 3

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def xmlInitStarted(self, elemBuilder):
        self.saveSettingsInContext()

        if self.hasSetting('name'):
            self.mode = self._StoringMode
            self.setSetting('ctxelem', self.getStyleSetting('name'))
        elif self.hasSetting('expand'):
            self.mode = self._ExpandingMode
            self.setSetting('unravel', 'down')
        elif self.hasSetting('invoke'):
            self.mode = self._InvokingMode
            self.setSetting('unravel', 'down')
        else:
            raise RuntimeError, "%r node must have one attribute in ['name','expand','invoke']" % self.__class__.__name__

        elemBuilder.pushXMLFactories(self.xmlFactories)
        return CSSSkinElement.xmlInitStarted(self, elemBuilder)

    def xmlBuildComplete(self, elemBuilder):
        elemBuilder.popXMLFactories()

        if self.mode == self._StoringMode:
            self.templateStore(elemBuilder)
        elif self.mode == self._ExpandingMode:
            self.templateExpand(elemBuilder)
        elif self.mode == self._InvokingMode:
            self.templateInvoke(elemBuilder)
        else:
            raise RuntimeError, "Invalid mode %r" % (self.mode,)

        self.removeSettingsInContext()
        CSSSkinElement.xmlBuildComplete(self, elemBuilder)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Protected Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def templateStore(self, elemBuilder):
        self.setObject(self.getStyleSetting('name'))

    def templateExpand(self, elemBuilder):
        invokename = '::invoke:' + self.getStyleSetting('expand')
        templateInner = self.getContextVar(invokename)
        templateInner.restoreChildren(elemBuilder)

    def templateInvoke(self, elemBuilder):
        templateOuter = self.getStyleSettingInContext('invoke')
        self.invokeRestoreable(elemBuilder, templateOuter, self.xmlParent())

