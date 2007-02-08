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

from sets import Set

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Constants / Variables / Etc. 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

base = Set(['TG'])
common = base | Set(['TG.common'])
introspection = base | Set(['TG.introspection'])
algorithms = base | Set(['TG.algorithms'])
w3c = common | Set(['TG.w3c'])

notifications = common | Set([
    'TG.notifications',
    'TG.notifications.engine',
    ])

uriResolver = w3c | Set([
    'TG.uriResolver',
    'TG.uriResolver.fileobj',
    ])

skinning = introspection | w3c | uriResolver | Set([
    'TG.skinning',
    'TG.skinning.engine',
    'TG.skinning.common',
    'TG.skinning.common.skin',
    'TG.skinning.common.python',
    'TG.skinning.common.xmlNode',
    'TG.skinning.toolkits',
    ])

guiTools = common | Set([
    'TG.guiTools',
    'TG.guiTools.wx',
    'TG.guiTools.win32',
    ])

wxPythonSkin = (notifications | skinning | guiTools 
    | Set([
    'TG.skinning.toolkits.wx',
    'TG.skinning.toolkits.wx.events',
    'TG.skinning.toolkits.wx.frames',
    'TG.skinning.toolkits.wx.layouts',
    'TG.skinning.toolkits.wx.widgets',
    'TG.skinning.toolkits.wx.tools',
    'TG.skinning.toolkits.wx.docking',
    'TG.skinning.toolkits.wx.external',
    ]))

all = (common | algorithms | w3c | notifications | uriResolver | skinning | guiTools | wxPythonSkin)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == "__main__":
    values = [(n,v) for n,v in vars().items() if n != 'Set' and not n.startswith('_')]
    values.sort()

    print "Package Listing:"
    print "================"
    for name, value in values:
        if isinstance(value, Set):
            print '%s:' % (name,)
            value = list(value)
            value.sort()
            for v in value:
                print '   ', v
            print

