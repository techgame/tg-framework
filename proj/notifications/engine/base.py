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

from TG.notifications.engine.properties import NotificationPropertyFactory

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Notifications Interface
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class NotificationBase(NotificationPropertyFactory):
    """Abstract class for implementing the Subject/Observer or Publish/Subscribe pattern."""

    def _notify(self, *args, **kw):
        """Composed method for notifying a collection given access rules and passing explicit args, kw."""
        accessControl = self.getAccessControl()
        token = accessControl.acquire(self)
        if token:
            args, kw = self._notifyArgsKws(args, kw)
            try: 
                result = self._notifySinks(*args, **kw)
            finally: 
                accessControl.release(self, token)

            return self._notifyComplete(result, args, kw)
        else:
            return self._notifyAccessDenied(args, kw)

    def _notifyArgsKws(self, args, kw):
        return args, kw

    def _notifyComplete(self, result, args, kw):
        """Called after notifying sinks and releasing access control"""
        return result

    def _notifyAccessDenied(self, args, kw):
        """Called when access could not be acquired"""
        pass

    def _notifySinks(self, *args, **kw):
        """Notify each sink with pertinent info from args and kw"""
        raise NotImplementedError("Subclass responsibility")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getAccessControl(self):
        """Returns an instance implementing AccessControl"""
        raise NotImplementedError("Subclass responsibility")

    def getSinks(self):
        """Returns an instance implementing SinkCollection"""
        raise NotImplementedError("Subclass responsibility")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Notification Object Base
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class NotificationObjBase(NotificationBase):
    _savedArgKw = None

    def __init__(self, *args, **kw):
        self._savedArgKw = args, kw
    def _notifyArgsKws(self, args, kw):
        if self._savedArgKw:
            sargs, skw = self._savedArgKw
            args = sargs + args
            kw.update(skw)
        return args, kw

