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

import win32ui, win32uiole, pywintypes
from win32com.client import gencache
from win32com.client import dynamic

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Function Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def getAXControlCoClass(progOrClsID):
    try:
        coclass = gencache.GetClassForProgID(progOrClsID)
        if not coclass:
            # Well, we might not have a cached one... so lets go find the TypeLib
            dis = dynamic.Dispatch(pywintypes.IID(progOrClsID))
            tlbAttr = dis._lazydata_[0].GetContainingTypeLib()[0].GetLibAttr()
            # Now gencache it
            TLB = gencache.EnsureModule(tlbAttr[0], tlbAttr[1], tlbAttr[3], tlbAttr[4])
            # And try Aagain
            coclass = gencache.GetClassForProgID(progOrClsID)
            if not coclass:
                # Dang... still didn't work
                raise LookupError("ActiveX class not found for %r" % (progOrClsID, ))
        return coclass
    except pywintypes.com_error:
        raise LookupError("ActiveX class not found for %r" % (progOrClsID, ))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def getAXControlModule(progOrClsID):
    try:
        module = gencache.GetModuleForProgID(progOrClsID)
        if not module:
            # Well, we might not have a cached one... so lets go find the TypeLib
            dis = dynamic.Dispatch(pywintypes.IID(progOrClsID))
            tlbAttr = dis._lazydata_[0].GetContainingTypeLib()[0].GetLibAttr()
            # Now gencache it
            TLB = gencache.EnsureModule(tlbAttr[0], tlbAttr[1], tlbAttr[3], tlbAttr[4])
            # And try Aagain
            module = gencache.GetModuleForProgID(progOrClsID)
            if not module:
                # Dang... still didn't work
                raise LookupError("ActiveX class module not found for %r" % (progOrClsID, ))
        return module
    except pywintypes.com_error:
        raise LookupError("ActiveX class module not found for %r" % (progOrClsID, ))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

