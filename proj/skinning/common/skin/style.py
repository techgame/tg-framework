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

from TG.skinning.common.cssElement import CSSSkinElement

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CSSStyleElement(CSSSkinElement):
    content = ''

    def xmlAddData(self, elemBuilder, data, srcref):
        self.content += data

    def xmlInitFinalized(self, elemBuilder):
        CSSSkinElement.xmlInitFinalized(self, elemBuilder)

        role = self.getSetting('role', 'author')
        kwStylesheet = {role: None}
        updateCSSCascade = self.getContext().updateCSSCascade

        ref = self.getSettingRef()
        if ref:
            # parse the external stylesheet
            kwStylesheet[role] = self.getCSSParser().parseExternal(ref)
            # publish the stylesheet to the cssCascade
            updateCSSCascade(**kwStylesheet)

        if self.content:
            # parse the inline stylesheet
            kwStylesheet[role] = self.getCSSParser().parseWithSrcRef(self.content, self._settings.srcref)
            # free up context now that it is parsed
            del self.content 
            # publish the stylesheet to the cssCascade
            updateCSSCascade(**kwStylesheet)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class style(CSSStyleElement):
    pass

