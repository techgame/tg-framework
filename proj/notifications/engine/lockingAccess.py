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

import weakref
from base import AccessControlBase

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Lock(object):
    pass

class LockingAccess(AccessControlBase):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    LockFactory = Lock
    _locked = None

    raiseAccessException = True

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Access Rules 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def acquire(self, requester):
        if not self.isLocked():
            return self.lock()
        elif self.raiseAccessException: 
            raise self.AccessAcquireException("Access already acquired!")
        return False

    def release(self, requester, token):
        if self.isLocked():
            if token:
                del token
                return True
        elif self.raiseAccessException: 
            raise self.AccessReleaseException("Access released without being acquired!")
        return False

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Locking logic 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def lock(self):
        """Prevents observers of reference from being updated while a lock is held on the reference."""
        if self.isLocked():
            if self.raiseAccessException:
                raise self.AccessException("Lock has already been aquired")
            else:
                return self._locked()
        else:
            lockResult = self.LockFactory()
            self._locked = weakref.ref(lockResult, self._onTokenUnlock)
            return lockResult

    def isLocked(self):
        """Returns true if the reference is locked"""
        return self._locked is not None

    def _onTokenUnlock(self, lock):
        """Resets the lock when unused"""
        del self._locked

