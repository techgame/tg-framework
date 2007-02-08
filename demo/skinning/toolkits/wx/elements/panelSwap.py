#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from TG.skinning.toolkits.wx import wxSkinModel, XMLSkin

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

xmlSkin = XMLSkin("""<?xml version='1.0'?>
<skin xmlns='TG.skinning.toolkits.wx' xmlns:skin='TG.skinning.common.skin'>
    <style>
        layout.spaced * {
            layout-border: 'ALL, 5';
            }
    </style>
    <frame title='My Frame' show='1'>
        <panel>
            <layout>
                <layout layout-cfg='0,EXPAND'>
                    <button label='Red'>
                        <event>
                            ctx.dockableOne.dockTo(ctx.myDockhost)
                        </event>
                    </button>
                    <button label='Green'>
                        <event>
                            ctx.dockableTwo.dockTo(ctx.myDockhost)
                        </event>
                    </button>
                    <button label='Blue'>
                        <event>
                            ctx.dockableThree.dockTo(ctx.myDockhost)
                        </event>
                    </button>
                </layout>
                <panel>
                    <layout>
                        <dock-host single='True' ctxobj='myDockhost' />
                        <dockable ctxobj='dockableOne'>
                            <panel bgcolor='red'>
                                <layout css-class='spaced'>
                                    <layout>
                                        <reference ref='fileExplorer.skin'/>
                                    </layout>
                                </layout>
                            </panel>
                        </dockable>
                        <dockable ctxobj='dockableTwo'>
                            <panel bgcolor='green'>
                                <layout css-class='spaced'>
                                    <calendar layout-cfg='0,ALIGN_CENTER' />
                                </layout>
                            </panel>
                        </dockable>
                        <dockable ctxobj='dockableThree'>
                            <panel bgcolor='blue'>
                                <layout css-class='spaced'>
                                    <htmlwin layout-cfg='1,EXPAND'>
                                        <html xmlns='http://www.w3.org/1999/xhtml'>
                                            <body>
                                                <h1>This is a test</h1>
                                                <p>Does it work yet?</p>
                                            </body>
                                        </html>
                                    </htmlwin>
                                </layout>
                            </panel>
                        </dockable>

                        ctx.dockableOne.dockTo(ctx.myDockhost)
                    </layout>
                </panel>
            </layout>
        </panel>
    </frame>
</skin>
""")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    wxSkinModel.fromSkin(xmlSkin).skinModel()

