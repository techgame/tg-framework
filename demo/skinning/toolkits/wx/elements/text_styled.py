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

    <frame title='My Frame' show='1'>
        <layout>
            #test
            <panel>
                <layout>
                    <text-styled layout-cfg='1,EXPAND|ALL,5'>
                        # ported from the wxPython demo
                        import keyword
                        obj.SetLexer(STC_LEX_PYTHON)
                        obj.SetKeyWords(0, " ".join(keyword.kwlist))

                        obj.StyleClearAll()
                        obj.StyleSetSpec(STC_STYLE_DEFAULT,     "size:10")
                        obj.StyleSetSpec(STC_STYLE_LINENUMBER,  "back:#C0C0C0,size:10")
                        obj.StyleSetSpec(STC_STYLE_CONTROLCHAR, "face:Courier")
                        obj.StyleSetSpec(STC_STYLE_BRACELIGHT,  "fore:#FFFFFF,back:#0000FF,bold")
                        obj.StyleSetSpec(STC_STYLE_BRACEBAD,    "fore:#000000,back:#FF0000,bold")
                        obj.StyleSetSpec(STC_P_DEFAULT, "fore:#000000,size:10")
                        obj.StyleSetSpec(STC_P_COMMENTLINE, "fore:#007F00,size:10")
                        obj.StyleSetSpec(STC_P_NUMBER, "fore:#007F7F,size:10")
                        obj.StyleSetSpec(STC_P_STRING, "fore:#7F007F,size:10")
                        obj.StyleSetSpec(STC_P_CHARACTER, "fore:#7F007F,size:10")
                        obj.StyleSetSpec(STC_P_WORD, "fore:#00007F,bold,size:10")
                        obj.StyleSetSpec(STC_P_TRIPLE, "fore:#7F0000,size:10")
                        obj.StyleSetSpec(STC_P_TRIPLEDOUBLE, "fore:#7F0000,size:10")
                        obj.StyleSetSpec(STC_P_CLASSNAME, "fore:#0000FF,bold,underline,size:10")
                        obj.StyleSetSpec(STC_P_DEFNAME, "fore:#007F7F,bold,size:10")
                        obj.StyleSetSpec(STC_P_OPERATOR, "bold,size:10")
                        obj.StyleSetSpec(STC_P_IDENTIFIER, "fore:#000000,size:10")
                        obj.StyleSetSpec(STC_P_COMMENTBLOCK, "fore:#7F7F7F,size:10")
                        obj.StyleSetSpec(STC_P_STRINGEOL, "fore:#000000,back:#E0C0E0,eol,size:10")

                        obj.SetText(open('text_styled.py', 'r').read())
                        obj.Colourise(0, -1)
                    </text-styled>
                </layout>
            </panel>
        </layout>
        obj.Center()
    </frame>

</skin>
""")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    wxSkinModel.fromSkin(xmlSkin).skinModel()


