#!/usr/bin/env python
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
        frame>layout>panel {layout-cfg:'1,EXPAND'}
        image-list>image-art {size:inherit}
    </style>

    <frame title='My Frame' show='1'>
        <layout>
            <panel>
                <layout>
                    <list style="LC_REPORT" layout-cfg='1,EXPAND'>
                        <column col='0' text='Title' width='100'>
                            <event>
                                MessageBox('You clicked on the "Title" column!', parent=elem.getParentFrame())
                            </event>
                        </column>
                        <list-column col='1' text='Detail' width='200' proportion='1'>
                            <event>
                                MessageBox('You clicked on the "Detail" column!', parent=elem.getParentFrame())
                            </event>
                        </list-column>
                        <column col='2' text='Amount' width='100' align='LIST_FORMAT_RIGHT' >
                            <event>
                                MessageBox('You clicked on the "Amount" column!')
                            </event>
                        </column>

                        <image-list size='32,32' for='normal'>
                            <image-art art='ART_INFORMATION'/>
                            <image-art art='ART_QUESTION'/>
                            <image-art art='ART_WARNING' />
                            <image-art art='ART_ERROR' />
                        </image-list>
                        <image-list size='16,16' for='small'>
                            <image-art art='ART_INFORMATION'/>
                            <image-art art='ART_QUESTION'/>
                            <image-art art='ART_WARNING' />
                            <image-art art='ART_ERROR' />
                        </image-list>

                        <list-item text='Item One'/>
                        <list-item text='Item One, in column B' col='1' />
                        <list-item text='$42.50' col='2' />

                        <event type='EVT_LIST_ITEM_SELECTED'>
                            print "in Skin..."
                            evt.Skip()
                        </event>
                        <item text='Second item' image='1' fgcolor='red'>
                            <event type='EVT_LIST_ITEM_SELECTED'>
                                print "in Skin, under item!"
                                import time
                                listCtrl = evt.GetEventObject()
                                listCtrl.SetItemText(obj.GetId(), time.asctime())
                                evt.Skip()
                            </event>
                        </item>
                        <item text='Second item, in column B' col='1' image='1' />
                        <item text='$76.95' col='2' />

                        <item text='Third is fun' fgcolor='#808' bgcolor='#8F8' font='bold italic large Tahoma, serif'/>
                        <item text='$0.00' col='2'/>

                        <menu-popup>
                            <menu-item text='List'>
                                <event>
                                    ctx.popup.window.SetSingleStyle(LC_LIST)
                                </event>
                            </menu-item>
                            <menu-item text='Icon'>
                                <event>
                                    ctx.popup.window.SetSingleStyle(LC_ICON)
                                </event>
                            </menu-item>
                            <menu-item text='Small Icon'>
                                <event>
                                    ctx.popup.window.SetSingleStyle(LC_SMALL_ICON)
                                </event>
                            </menu-item>
                            <menu-item text='Report'>
                                <event>
                                    ctx.popup.window.SetSingleStyle(LC_REPORT)
                                </event>
                            </menu-item>
                            <event>
                                obj.popupEvt(evt)
                            </event>
                            <event type='EVT_COMMAND_RIGHT_CLICK'>
                                # on windows, ListCtrls don't like normal EVT_RIGHT_UP messages...
                                pos = obj.window.ScreenToClient(GetMousePosition())
                                obj.popup(pos)
                            </event>
                        </menu-popup>
                    </list>
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


