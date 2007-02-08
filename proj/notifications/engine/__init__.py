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

import base
import access
import store
import notify

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Summary Definition
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class PlugableNotification(
        notify.PlugableNotify, 
        store.PlugableSinkCollectionExtended, 
        access.PlugableAccessControl, 
        base.NotificationObjBase):

    """A plugable Notification implementation.
    
    Very versatile noticiation combination that has plugable implementations of
    the notify strategy, store collection, and access control.
    
    """
PlugableNotificationBase = PlugableNotification

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Notification(PlugableNotification):
    """Makes notify() the notify interface"""
    def notify(self, *args, **kw):
        return self._notify(*args, **kw)

