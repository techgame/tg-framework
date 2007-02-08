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

from TG.common import path
from TG.skinning.toolkits.wx import wxSkinModel, XMLSkin

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Constants / Variables / Etc. 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

xmlSkin = XMLSkin("""<?xml version='1.0'?>
<panel xmlns='TG.skinning.toolkits.wx' xmlns:skin='TG.skinning.common.skin'>
    <layout>
        <button class='alignCenter' label='Top' >
            <event>ctx.model.getDockable().dockTo(ctx.dhTop)</event>
        </button>
        <layout>
            <button class='alignCenter' label='Left' >
                <event>ctx.model.getDockable().dockTo(ctx.dhLeft)</event>
            </button>

            <layout>
                <listbox layout-cfg='1,EXPAND'>
                    for choice in ctx.model.getDockableNames():
                        obj.Append(choice)

                    <event>
                        ctx.model.setDockableChoice(evt.GetString())
                        ctx.model.getDockable().dockTo(ctx.dhCenter)
                    </event>
                </listbox>

                <spacer />

                <notebook layout-cfg='3,EXPAND'>
                    <dock-host-book ctxobj='dhCenter' model='ctx.model' />
                </notebook>

                <spacer />

                <layout layout-cfg='0,EXPAND'>
                    <spacer layout-cfg='1,EXPAND'/>

                    <button label='Toggle'>
                        <event>ctx.model.getDockable().dockToggle()</event>
                    </button>

                    <spacer layout-cfg='1,EXPAND'/>

                    <button label='Center'>
                        <event>ctx.model.getDockable().dockTo(ctx.dhCenter)</event>
                    </button>

                    <spacer layout-cfg='1,EXPAND'/>

                    <button label='Free'>
                        <event>
                            dockable = ctx.model.getDockable()
                            dockable.undock()
                            ctx.floatFrame.lockTo(ctx.frame, 'top,right', 'bottom')
                            dockable.dockTo(ctx.dhFloat)
                            ctx.floatFrame.SetFocus()
                        </event>
                    </button>

                    <spacer layout-cfg='1,EXPAND'/>
                </layout>
            </layout>

            <button class='alignCenter' label='Right' >
                <event>ctx.model.getDockable().dockTo(ctx.dhRight)</event>
            </button>
        </layout>
        <button class='alignCenter' label='Bottom' >
            <event>ctx.model.getDockable().dockTo(ctx.dhBottom)</event>
        </button>
    </layout>

    <frame-mini ctxobj='floatFrame'>
        <layout>
            <dock-host ctxobj='root.dhFloat' hide-empty='True' model='ctx.model' />
        </layout>

        <event>
            if evt.CanVeto():
                obj.Hide()
                evt.Veto()
            else: evt.Skip()
        </event>
    </frame-mini>
</panel>
""")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Model
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class DockingModel(wxSkinModel):
    xmlModelSkin = xmlSkin
    skinPath = path.path('.')

    def getDockableNames(self):
        self.dockableSkinChoices = {}
        for skinFile in self.skinPath.files("*.skin"):
            self.dockableSkinChoices[skinFile] = skinFile
        self.dockableChoice = skinFile
        return self.dockableSkinChoices.keys()

    def getDockable(self):
        result = self.dockableSkinChoices[self.dockableChoice]
        if isinstance(result, basestring):
            result = self.ctx.skinner.skinFile(result.open(), model=self)
            result = result.ctx.dockable
            self.dockableSkinChoices[self.dockableChoice] = result
        return result

    def setDockableChoice(self, choice):
        if choice in self.dockableSkinChoices:
            self.dockableChoice = choice

    def setDockable(self, dockable):
        self.dockableChoice = None
        self.dockableSkinChoices[self.dockableChoice] = dockable

