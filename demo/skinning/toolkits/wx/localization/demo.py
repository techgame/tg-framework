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

import os
import locale
import gettext

from TG.skinning.toolkits.wx import wxSkinModel, XMLSkin

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Constants / Variables / Etc. 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# TODO: we need something that can parse XML for the strings that need localization

xmlSkin = XMLSkin("""<?xml version='1.0'?>
<skin xmlns='TG.skinning.toolkits.wx'>
    <style>
        frame {size:'200,200'}
    </style>

    <frame class='main' title='My Frame' show='1'>
        <layout>
            <panel>
                <layout>
                    <label text='My Label' />
                    <textbox text='My Textbox' />
                </layout>
            </panel>
        </layout>
    </frame>
</skin>
""")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    translation = gettext.translation('messages', './locale', languages=['de', 'fr', 'en'])
    translation.install()

    print
    print '_(My Frame):', _('My Frame')
    print '_(My Label):', _('My Label')
    print '_(My Textbox):', _('My Textbox')
    print
    print 'gettext.gettext(My Frame):', gettext.gettext('My Frame')
    print 'gettext.gettext(My Label):', gettext.gettext('My Label')
    print 'gettext.gettext(My Textbox):', gettext.gettext('My Textbox')
    print

    wxSkinModel.fromSkin(xmlSkin).skinModel(gettext=_)

