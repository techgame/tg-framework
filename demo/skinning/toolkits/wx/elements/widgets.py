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
        * { bgcolor:inherit; fgcolor:inherit; }

        frame {
            frame-main: True; 
            locking: True; 
            show: True;
            /* bgcolor: #ddf; */
        }

        frame>layout {layout-cfg:'1,EXPAND'}
        layout>layout {layout-cfg:'1,EXPAND|ALL,5'}
        frame>layout>panel {layout-cfg:'1,EXPAND'; layout-border: None}
        frame-popup>layout>panel {layout-cfg:'1,EXPAND'; layout-border: None}

        layout>*:first-child {layout-cfg:'0,EXPAND'; layout-border:'ALL,5';}
        layout>* {layout-cfg:'0,EXPAND'; layout-border:'LEFT|RIGHT|BOTTOM,5';}

        image-list>image-art {size:inherit}
    </style>

    <frame title='My Frame' >
        <menubar>
            <menu>
                <reference ref='commonMenu.skin'/>
            </menu>
        </menubar>

        <!--<toolbar> </toolbar>-->

        <layout>
            <panel>
                print
                elem.debugCtx()
                print
                elem.debugNameStack()
                print
                elem.debugCSS()
                print

                <grabber/>

                <layout>
                    <layout layout-cfg='2,EXPAND'>
                        <groupbox label='My Groupbox' layout-cfg='1,EXPAND'>
                            <layout>
                                <password text='Some stuff' tooltip='Your password\\n\\tplease!'>
                                    <event>print 'What are you doing putting your password into a foreign app?'</event>
                                </password>

                                <choice select='-1' choices='choice item 1, choice item 2  , choice item 3'>
                                    <event>print "You selected My Choice!:", evt.GetString()</event>
                                </choice>

                                <checklist select='-2' choices='item 1, item 2  , item 3'>
                                    <event>
                                        idx = evt.GetSelection()
                                        if obj.IsChecked(idx):
                                            print "You checked My CheckList!:", obj.GetString(idx)
                                        else:
                                            print "You UN checked My CheckList!:", obj.GetString(idx)
                                    </event>

                                </checklist>

                                <listbox select='-2' choices='item 1, item 2  , item 3'>
                                    <event>print "You selected My ListBox!:", evt.GetString()</event>
                                </listbox>

                                <combobox select='-2'>
                                    for i,n in enumerate(vars(wx).keys()[:100]):
                                        obj.Append('%d: wx.%s' % (i, n))

                                    <event>print "You selected My ComboBox:", repr(evt.GetString())</event>
                                </combobox>

                                <textbox text='My Textbox'>
                                    <event>print "You edited My TextBox!:", evt.GetString()</event>
                                    <event type='EVT_TEXT_ENTER'>print "You entered '%s' into My TextBox!" % (evt.GetString(), )</event>
                                </textbox>

                                <hline/>

                                <label ctxobj='timerLabel' text="Timer response">
                                    <timer seconds='1'>
                                        <event>
                                            import time
                                            label = ctx.timerLabel
                                            label.SetLabel(time.asctime())
                                        </event>
                                    </timer>
                                    <timer seconds='0.5'>
                                        <event>
                                            import time
                                            label = ctx.timerLabel
                                            if label.GetForegroundColour() == (0,0,0):
                                                label.SetForegroundColour((0,0,255))
                                            else:
                                                label.SetForegroundColour((0,0,0))
                                            label.Refresh()
                                        </event>
                                    </timer>
                                </label>

                                <hline/>

                                <gauge value='15' range='20' size='200,20'/>

                                <htmlwin layout-cfg='1,EXPAND'>
                                    <html xmlns='http://www.w3.org/1999/xhtml'>
                                        <body>
                                            <h1>This is a test</h1>
                                            <p>Does it work yet?</p>
                                        </body>
                                    </html>
                                </htmlwin>
                            </layout>
                        </groupbox>
                        <layout layout-cfg='0,EXPAND'>
                            <groupbox label='Common Widgets'>
                                <layout>
                                    <label text='My Label'>
                                        <event>print "You clicked My Label!"</event>
                                    </label>

                                    <layout layout-cfg='0,EXPAND'>
                                        <button label='My Button' layout-cfg='1,EXPAND'>
                                            <event>print "You pressed My Button:", evt.GetEventObject() is obj</event>
                                        </button>

                                        <button-toggle label='My Toggle Button' layout-cfg='1,EXPAND'>
                                            <event>print "You pressed My Toggle Button:", evt.GetInt()</event>
                                        </button-toggle>
                                    </layout>

                                    <hline/>

                                    <checkbox label='My Checkbox' >
                                        <event>print "You pressed My Checkbox:", repr(evt.GetInt())</event>
                                    </checkbox>

                                    <radio value='1' label='My Radio Choice A'>
                                        <event>print "You selected My Radio Choice A:", repr(evt.GetInt())</event>
                                    </radio>
                                    <radio value='0' label='My Radio Choice B'>
                                        <event>print "You selected My Radio Choice B:", repr(evt.GetInt())</event>
                                    </radio>
                                    <radio value='0' label='My Radio Choice C'>
                                        <event>print "You selected My Radio Choice C:", repr(evt.GetInt())</event>
                                    </radio>

                                    <slider value='40'>
                                        <event>print "You used My Slider:", repr(evt.GetInt())</event>
                                    </slider>

                                    <scrollbar thumb='5' max='20'>
                                        <event>print "You used My Scrollbar:", repr(evt.GetInt())</event>
                                    </scrollbar>
                                </layout>
                            </groupbox>

                            <hline />

                            <calendar>
                                <event>print "You selected My Calendar!:", evt.GetDate()</event>
                            </calendar>

                            <button label='Show My Popup'>
                                <event>
                                    myPopup = ctx.myPopup
                                    myPopup.lockTo(obj, 'bottom,cHoriz')
                                    myPopup.Show()
                                </event>
                            </button>

                            <popup ctxobj='myPopup'>
                                <layout>
                                    <button label='My Popup Button' >
                                        <event>print "You pressed My Popup Button:", evt.GetEventObject()</event>
                                    </button>
                                    <slider ctxobj='myPopup.slider' value='40'>
                                        <event>print "You used My Popup Slider:", repr(evt.GetInt())</event>
                                    </slider>
                                </layout>

                                def onPopupShowing(self):
                                    print "Showing!", self.slider.GetValue()
                                obj.onShowing = onPopupShowing
                                def onPopupHiding(self):
                                    print "Hiding!", self.slider.GetValue()
                                obj.onHiding = onPopupHiding
                            </popup>
                        </layout>

                        <layout>
                            <reference ref='fileExplorer.skin'/>

                            <text-styled layout-cfg='1,EXPAND'>
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

                                obj.SetText(open('widgets.py', 'r').read())
                                obj.Colourise(0, -1)
                            </text-styled>
                        </layout>
                    </layout>
                    <notebook layout-minsize='400,300'>
                        <image-list size='16,16'>
                            <image-art art='ART_INFORMATION'/>
                            <image-art art='ART_QUESTION'/>
                            <image-art art='ART_WARNING'/>
                            <image-art art='ART_ERROR'/>
                        </image-list>

                        <panel-scrolled page-name='Scrolled Panel Page' page-image='0'>
                            <layout>
                                <reference ref='largeLayout.skin'/>
                            </layout>
                        </panel-scrolled>

                        <calendar page-name='Calendar Page' page-image='1' />

                        <scrollwin page-name='Scolled Page' page-image='2'>
                            <layout>
                                <reference ref='largeLayout.skin'/>
                            </layout>
                        </scrollwin>
                    </notebook>
                </layout>
            </panel>
        </layout>

        <!--<statusbar> </statusbar>-->

        obj.Center()
    </frame>
</skin>
""")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    wxSkinModel.fromSkin(xmlSkin).skinModel()

