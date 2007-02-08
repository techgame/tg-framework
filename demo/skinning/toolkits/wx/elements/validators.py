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

from TG.skinning.toolkits.wx import wxSkinModel, XMLSkin

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Constants / Variables / Etc. 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

xmlSkin = XMLSkin("""<?xml version='1.0'?>
<skin xmlns='TG.skinning.toolkits.wx'>
    <style>
        frame {frame-main:1; locking:1; size:'800,600'}
        frame>layout {layout-cfg:'1,EXPAND'}
        layout>layout {layout-cfg:'0,EXPAND'}
        frame>layout>panel {layout-cfg:'1,EXPAND'}
    </style>

    <dialog title='My Frame' show='True'>
        <layout>
            <label text='Type "Please" to pass'/>
            <text>
                <validator>
                    if obj.GetValue().lower() == 'please':
                        obj.SetBackgroundColour(SystemSettings_GetColour(SYS_COLOUR_WINDOW))
                        result = True
                    else:
                        obj.SetBackgroundColour('#FFDDDD')
                        result = False
                    obj.Refresh()
                    print "Validate!:", result

                    return result
                    <event>
                        # reject certain keys by eating the event (i.e. call evt.Skip(False))
                        evt.Skip(True)
                        key = evt.KeyCode()
                        if 31 &lt; key &lt; 128:
                            if not chr(key).isalpha():
                                evt.Skip(False)
                    </event>
                    <event type='EVT_KEY_UP'>
                        if obj.GetValue().lower() == 'please':
                            obj.SetBackgroundColour('#DDFFDD')
                        elif evt.KeyCode() != WXK_RETURN:
                            obj.SetBackgroundColour(SystemSettings_GetColour(SYS_COLOUR_WINDOW))
                        obj.Refresh()
                        evt.Skip()
                    </event>
                </validator>
            </text>

            <button label='Ok' default='True' wxid='ID_OK'>
                <event>
                    dialog = ctx.dialog
                    if dialog.Validate():
                        dialog.SetReturnCode(True)
                        dialog.Close()
                </event>
            </button>
            <button label='Cancel' wxid='ID_CANCEL'>
                <event>
                    print "on CANCEL:"
                    ctx.dialog.Close()
                </event>
            </button>
        </layout>

        obj.Center()

        <event>
            print "Closing!"
            ctx.application.Exit()
            evt.Skip()
        </event>
    </dialog>
</skin>
""")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    wxSkinModel.fromSkin(xmlSkin).skinModel()


