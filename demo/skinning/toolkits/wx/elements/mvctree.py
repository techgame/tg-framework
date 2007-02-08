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

    <frame title='MVCTree Frame' show='1'>
        <layout>
            <panel bgcolor="red">
                <layout layout-cfg="1,EXPAND">
                    <mvctree ctxobj="aTree">
                        obj.SetAssumeChildren(True)
                        from wx.lib import mvctree as tree
                        import os
                        obj.SetModel(tree.FSTreeModel(os.path.normpath(os.getcwd() + os.sep +'..')))

                        #Uncomment this to enable live filename editing!
                        #obj.AddEditor(FileEditor(obj))

                        obj.SetMultiSelect(True)
                        <event type="EVT_MVCTREE_SEL_CHANGING">
                            print "Selection changing"
                            evt.Skip()
                        </event>
                        <event type="EVT_MVCTREE_SEL_CHANGED">
                            print "Selection changed"
                            evt.Skip()
                        </event>
                        <event type="EVT_MVCTREE_ITEM_EXPANDED">
                            print "Item expanded"
                            evt.Skip()
                        </event>
                        <event type="EVT_MVCTREE_ITEM_COLLAPSED">
                            print "Item Collapsed"
                            evt.Skip()
                        </event>
                        <event type="EVT_MVCTREE_ADD_ITEM">
                            print "Add Item"
                            evt.Skip()
                        </event>
                        <event type="EVT_MVCTREE_DELETE_ITEM">
                            print "Delete Item"
                            evt.Skip()
                        </event>
                        <event type="EVT_MVCTREE_KEY_DOWN">
                            print "Key down"
                            evt.Skip()
                        </event>
                    </mvctree>
                    obj.Layout()
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

