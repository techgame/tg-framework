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

import re
import datetime

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

_pISODate = (r'(\d{4})-(\d{2})-(\d{2})')# year-month-day 
reISODate = re.compile(_pISODate)

_pISOTime = (
        r'(\d{2}):(\d{2})' +                    # hours:minutes 
        r'(?::(\d{2})(\.\d{0,6})?)?' +      # :seconds (.microseconds) 
        r'(?:[+-]\d{2}:\d{2})?'                 # timezone offset (no matching)
        #r'(?:([+-])(\d{2}):(\d{2}))?'          # timezone offset (matching)
        )
reISOTime = re.compile(_pISOTime)

_pISOFormat = (_pISODate + '(?:\\D' + _pISOTime + ')?')
reISOFormat = re.compile(_pISOFormat)

#~ iso formated time information ~~~~~~~~~~~~~~~~~~~~
def parseISOFormat(isofmt, reFormat=reISOFormat):
    """ISO 8601 format, HH:MM:SS.ssssss
    returns datetime.time(HH, MM, SS, ssssss)"""
    matches = reFormat.match(isofmt)
    if not matches:
        return

    for x in matches.groups():
        if x is None:
            break
        elif x.startswith('.'):
            x = x[1:].ljust(6, '0')
        yield int(x)

def timeFromISO(isofmt, reISOFormat=reISOTime):
    """ISO 8601 format, HH:MM:SS.ssssss
    returns datetime.time(HH, MM, SS, ssssss)"""
    values = list(parseISOFormat(isofmt, reISOFormat))
    if not values: 
        raise ValueError("Invalidly formatted ISO time string: %r" % (isofmt,), isofmt)
    return datetime.time(*values)

def dateFromISO(isofmt, reISOFormat=reISODate):
    """ISO 8601 format, YYYY-MM-DD
    returns datetime.date(YYYY, MM, DD)"""
    values = list(parseISOFormat(isofmt, reISOFormat))
    if not values: 
        raise ValueError("Invalidly formatted ISO date string: %r" % (isofmt,), isofmt)
    return datetime.date(*values)

def datetimeFromISO(isofmt, reISOFormat=reISOFormat):
    """ISO 8601 format, YYYY-MM-DDTHH:MM:SS.ssssss
    returns datetime.datetime(YYYY, MM, DD, HH, MM, SS, ssssss)"""
    values = list(parseISOFormat(isofmt, reISOFormat))
    if not values: 
        raise ValueError("Invalidly formatted ISO date time string: %r" % (isofmt,), isofmt)
    return datetime.datetime(*values)
fromiso = fromISO = datetimeFromISO

