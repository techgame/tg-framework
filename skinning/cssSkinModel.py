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

import sets
from TG.skinning.common import css
from TG.skinning.skinModel import SkinModel, XMLSkin

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ CSS Skin Model
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CSSSkinModel(SkinModel):
    """Adds CSS-awareness to SkinModel.

    To add to cssMediumSet::
        cssMediumSet = CSSSkinModel.cssMediumSet.copy()
        cssMediumSet.update('myMedium')

    To add to cssCascade::
        cssCascade = CSSSkinModel.cssCascade.copyWithUpdate(
                userAgent='#myStyle {myAttribute: myValue}')
    """

    cssMediumSet = sets.Set()
    cssCascade = css.CSSCascadeStrategy(author=None, user=None, userAgent=None)

    def _xmlSkinnerInitialize(self, skinner):
        SkinModel._xmlSkinnerInitialize(self, skinner)
        self.setCSSOptions(skinner)

    def setCSSOptions(self, skinner):
        if self.cssMediumSet:
            skinner.updateCSSMediumSet(self.getCSSMediumSet())

        cssCascade = self.getCSSCascade()
        if cssCascade is not None:
            cssCascade = cssCascade.copy()
            cssCascade.setParser(skinner.getCSSParser())
            context = skinner.getContext(True)
            context.setCSSCascade(cssCascade)
        return cssCascade

    def getCSSMediumSet(self):
        return self.cssMediumSet
    def getCSSCascade(self):
        return self.cssCascade

