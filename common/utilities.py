#!/usr/bin/env python
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##~ Copyright (C) 2002-2004  TechGame Networks, LLC.
##~ 
##~ This library is free software; you can redistribute it and/or
##~ modify it under the terms of the BSD style License as found in the 
##~ LICENSE file included with this distribution.
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""Just a handy sub-tool set of tools.  They just clean up the code a bit more..."""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import sys
import os
import re
import time
import itertools
import random

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def boolFromStr(value):
    value = value.lower()
    if value in ('', '0', 'false', 'no', 'none'):
        return False
    if value in ('1', 'true', 'yes'):
        return True
    return bool(int(value))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def textWiggler(ticker='<-*->', w=80, fmt='\r|%s|\r'):
    i = 0
    wmt = w/2 + len(ticker) - 2
    while 1:
        i += 1
        l = abs(wmt - (i % (2*wmt)))
        r = wmt - l
        mystr = ('%s%s%s' % (' '*l, ticker, ' '*r))
        yield fmt % (mystr,)
textWigglerGenerator = textWiggler

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def cleanUpStrLst(datalst, FilterResult=0):
    """Strips characters from a list of strings, and drops subsequent empty strings.

    >>> cleanUpStrLst(["   this  ", "  is  ", " \\t fun \\t \\r", "  \\n \\r \\t test\\t\\t"])
    ['this', 'is', 'fun', 'test']
    """
    result = map(str.strip, datalst)
    if FilterResult:
        return filter(None, result)
    else: return result

def joinClean(joinstr, data, *args, **kw):
    """Uses cleanUpStrLst, then joins the result using joinstr.
    If data is simply a string, then the data is splitup using strToList.

    >>> joinClean(".", ["   this  ", "  is  ", " \\t fun \\t \\r", "  \\n \\r \\t test\\t\\t"])
    'this.is.fun.test'
    >>> joinClean("-", "data, , fun  ,   data   ,   oh\\t\\t\\t ,please  \\t, \\r\\n can \\t  ,  I have more data!   ")
    'data--fun-data-oh-please-can-I have more data!'

    """
    if isinstance(data, list):
        return joinstr.join(cleanUpStrLst(data, *args, **kw))
    elif isinstance(data, (str, unicode)):
        return joinstr.join(strToList(data, *args, **kw))

def strToList(data, splitchar=',', *args, **kw):
    """Splits a dilimited string, then runs the result through cleanUpStrLst.

    >>> strToList("data, , fun  ,   data   ,   oh\\t\\t\\t ,please  \\t, \\r\\n can \\t  ,  I have more data!   ")
    ['data', '', 'fun', 'data', 'oh', 'please', 'can', 'I have more data!']
    """

    return cleanUpStrLst(data.split(splitchar), *args, **kw)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ MAC Address from process tools
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__MACAddresses = None

def getMACAddress(idx=0):
    return getAllMACAddresses()[idx]

def getAllMACAddresses():
    global __MACAddresses
    if __MACAddresses is None:
        __MACAddresses = _getSystemMACAddress()
    return __MACAddresses

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

reMACAddress = re.compile('((?:[0-9a-fA-F]{2}[:-]){5}[0-9a-fA-F]{2})')
def _normalizeMACAddress(mac):
    return mac.replace('-', ':')

if sys.platform.startswith('win'):
    def _getSystemMACAddress():
        data = os.popen('ipconfig /all').read()
        return map(_normalizeMACAddress, reMACAddress.findall(data))
else:
    def _getSystemMACAddress():
        data = os.popen('ifconfig -a').read()
        return map(_normalizeMACAddress, reMACAddress.findall(data))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Unique ID Generator
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def uniqueID(prefix='', counter=None):
    if counter is None:
        counter = itertools.count(0)
    mac = getMACAddress().replace(':', '')
    now = int(time.time()*65536)
    rand = random.randint(0, 0xffff)
    idstr = '%s%s%s:%08X:%04X:%%s' % (prefix, prefix and ':' or '', mac, now, rand)

    for count in counter:
        yield idstr % count

