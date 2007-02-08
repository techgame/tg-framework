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
        frame {frame-main:1; locking:1; }
        frame>layout {layout-cfg:'1,EXPAND'}
        layout>layout {layout-cfg:'1,EXPAND'}
        frame>layout>panel {layout-cfg:'1,EXPAND'}
    </style>

    <frame title='Media Control Frame' show='1'>
        <layout>
            <panel>
                <layout>
                    <layout layout-cfg="1,EXPAND">
                        <media ctxobj="movie" playercontrols="True" >
                            obj.Load('Zero_to_130.mpg')
                            <event>
                                print "It's Stopped:", obj.GetState()
                                evt.Skip()
                            </event>
                            <event type="EVT_MEDIA_LOADED">
                                print "The Media Loaded!", obj.GetState()
                            </event>
                        </media>
                    </layout>
                    <layout orient="HORIZONTAL" layout-cfg="0,EXPAND"> 
                        <button label="Play">
                            <event>
                                ctx.movie.Play()
                            </event>
                        </button>
                        <button label="Pause">
                            <event>
                                ctx.movie.Pause()
                            </event>
                        </button>
                        <button label="Stop">
                            <event>
                                ctx.movie.Stop()
                            </event>
                        </button>
                    </layout>
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
    wxSkinModel.fromSkin(xmlSkin).skinModel()

