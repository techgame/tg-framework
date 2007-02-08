##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##~ Copyright (C) 2002-2004  TechGame Networks, LLC.
##~ 
##~ This library is free software; you can redistribute it and/or
##~ modify it under the terms of the BSD style License as found in the 
##~ LICENSE file included with this distribution.
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Access Control
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class AccessException(Exception): 
    pass
class AccessAcquireException(AccessException):
    pass
class AccessReleaseException(AccessException):
    pass

class AccessControlBase(object):
    AccessException = AccessException
    AccessAcquireException = AccessAcquireException
    AccessReleaseException = AccessReleaseException

    def acquire(self, requester):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

    def release(self, requester, token):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Access Control Implementations
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class IgnoreAccess(AccessControlBase):
    def acquire(self, requester):
        return True

    def release(self, requester, token):
        pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ProtectiveAccess(AccessControlBase):
    raiseAccessException = True
    acquired = False

    def acquire(self, args, kw):
        if not self.acquired:
            self.acquired = True
            return True # Allow notification to commence
        elif self.raiseAccessException: 
            raise self.AccessAcquireException("Access already acquired!")
        return False

    def release(self, requester, token):
        if self.acquired:
            if token:
                self.acquired = False
                return True
        elif self.raiseAccessException: 
            raise self.AccessReleaseException("Access released without being acquired!")
        return False

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ NotificationBase Mixins
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class PlugableAccessControl(object):
    """For mixing in with Notification classes"""
    _accessControl = IgnoreAccess()

    def getAccessControl(self):
        """Returns an instance implementing AccessControl"""
        if self._accessControl is None:
            self.createAccessControl()
        return self._accessControl
    def setAccessControl(self, accessControl):
        """Sets an instance implementing AccessControl"""
        self._accessControl = accessControl

    def createAccessControl(self):
        accessControl = self.AccessControlFactory()
        self.setAccessControl(accessControl)
        return accessControl

