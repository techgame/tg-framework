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

from TG.skinning.engine.xmlSkinner import XMLFactory

from TG.skinning import resolvers
from TG.skinning.cssSkinModel import CSSSkinModel as _CSSSkinModelBase
from TG.skinning.engine import XMLFactory, XMLSkinner, XMLSkin
from TG.skinning.common import skin as CommonSkin

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Constants / Variables / Etc. 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

namespace = XMLFactory.xmlnsFromName(__name__)
namespaceSynonyms = {
    }

moduleCategories = (
    '',
    'widgets',
    'layers',
    )

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def createXMLFactory(namespace=namespace):
    return XMLFactory.HierarchyNodeImport(__name__, moduleCategories)

def install(builder, namespace=namespace):
    builder.xmlFactories.addFactory(namespace, createXMLFactory(namespace))
    builder.xmlnsSynonyms.update(namespaceSynonyms)

class RenderSkinModel(_CSSSkinModelBase):
    xmlSkinnerInstalls = [install, CommonSkin.install]

