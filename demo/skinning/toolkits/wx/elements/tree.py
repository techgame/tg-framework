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
                    <tree layout-cfg='1,EXPAND'>
                        <image-list size='32,32'>
                            <image-art art='ART_INFORMATION'/>
                            <image-art art='ART_QUESTION'/>
                            <image-art art='ART_WARNING' />
                            <image-art art='ART_ERROR' />
                        </image-list>

                        <tree-item text='Root Item' expanded='1' image='0' image-selected='1'>
                            <tree-item text='Child One' image='1' font='bold italic x-large Tahoma, serif'>
                                <tree-item text='Child One.One'/>
                                <tree-item text='Child One.Two' image='3'>
                                    <tree-item text='Child One.Two.One' image='0'/>
                                </tree-item>
                                <tree-item text='Child One.Three'/>
                            </tree-item>
                            <tree-item text='Child Two' image='2' bgcolor='orange'/>
                            <tree-item text='Child Three' image='3' font='bold xx-large Comic Sans, script' fgcolor='teal'>
                                <tree-item text='Child Three.One'/>
                                <tree-item text='Child Three.Two'/>
                                <tree-item text='Child Three.Three'/>
                            </tree-item>

                            <tree-item text='Double-click for the time!' image='1' font-size='x-large'>
                                <event>
                                    import time
                                    tree = evt.GetEventObject()
                                    tree.SetItemText(obj.GetTreeId(), time.asctime())
                                </event>
                            </tree-item>
                        </tree-item>
                    </tree>
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


