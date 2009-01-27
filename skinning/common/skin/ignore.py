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

from TG.w3c.xmlBuilder import ElementBase as _ElementBase
from TG.w3c.xmlClassBuilder import XMLFactory

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class IgnoreXML(_ElementBase):
    def xmlBuildCreate(self, elemBuilder): pass
    def xmlInitStarted(self, elemBuilder): pass
    def xmlPreAddElement(self, elemBuilder, name, attributes, srcref): pass
    def xmlAddElement(self, elemBuilder, node, elem, srcref): pass
    def xmlPostAddElement(self, elemBuilder, elem): pass
    def xmlAddData(self, elemBuilder, data, srcref): pass
    def xmlInitFinalized(self, elemBuilder): pass
    def xmlBuildComplete(self, elemBuilder): pass
    def xmlGetElement(self, elemBuilder): return self

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ignore(IgnoreXML):
    xmlFactories = XMLFactory.Collection({
        None: XMLFactory.Static(IgnoreXML),
        }).setName('ignore')

    def xmlInitStarted(self, elemBuilder):
        elemBuilder.pushXMLFactories(self.xmlFactories)
    def xmlInitFinalized(self, elemBuilder):
        elemBuilder.popXMLFactories()

