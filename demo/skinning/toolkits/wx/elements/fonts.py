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
        frame {frame-main:1; size:'1024,768'}
        line {layout-cfg: '0, EXPAND'}
        panel layout {layout-cfg: '1, EXPAND|ALL,10'}

        label {layout-cfg: '0, EXPAND'}
        textbox {layout-cfg: '0, EXPAND'}

        .font1 {font: bold xx-large Tahoma, serif}
        .font2 {font: x-large/110% "Courier New", serif}
        .font3 {font-family: "Comic Sans", cursive; font-size: 3em}
        .font4 {font-weight: lighter; font-family: fantasy; font-size: 0.5in}
    </style>

    <frame title='A skin full of fonts' show='1'>
        <layout fit='True'>
            <panel>
                <layout>
                    <line />
                    <layout orient='vertical'>
                        <textbox css-class='font1' text='The Quick Brown Fox Jumps Over The Lazy Dog' />
                        <spacer/>
                        <textbox css-class='font2' text='The Quick Brown Fox Jumps Over The Lazy Dog' />
                        <spacer/>
                        <textbox css-class='font3' text='The Quick Brown Fox Jumps Over The Lazy Dog' />
                        <spacer/>
                        <textbox css-class='font4' text='The Quick Brown Fox Jumps Over The Lazy Dog' />
                        <spacer/>
                        <textbox font='bold 20pt Tahoma, serif' text='The Quick Brown Fox Jumps Over The Lazy Dog' />
                        <spacer/>
                        <textbox css-class='font1' font-weight='light' font-size='1cm' text='The Quick Brown Fox Jumps Over The Lazy Dog' />
                        <spacer/>
                    </layout>
                    <spacer/>
                    <line />
                    <spacer/>
                    <layout orient='vertical'>
                        <label css-class='font1' text='The Quick Brown Fox Jumps Over The Lazy Dog' />
                        <spacer/>
                        <label css-class='font2' text='The Quick Brown Fox Jumps Over The Lazy Dog' />
                        <spacer/>
                        <label css-class='font3' text='The Quick Brown Fox Jumps Over The Lazy Dog' />
                        <spacer/>
                        <label css-class='font4' text='The Quick Brown Fox Jumps Over The Lazy Dog' />
                        <spacer/>
                        <label font='bold 20pt Tahoma, serif' text='The Quick Brown Fox Jumps Over The Lazy Dog' />
                        <spacer/>
                        <label css-class='font1' font-weight='light' font-size='1cm' text='The Quick Brown Fox Jumps Over The Lazy Dog' />
                        <spacer/>
                    </layout>
                    <line />
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

