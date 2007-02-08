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

from itertools import *

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

_sentinal = object()

def iterFilteredMapping(filterFunc, mapFunc, *args):
    return ifilter(filterFunc, imap(mapFunc, *args))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def iterBy2(iterable, start=_sentinal, end=_sentinal):
    iterable = iter(iterable)
    p = iterable.next()
    if start is not _sentinal:
        yield start, p
    for n in iterable:
        yield p, n
        p = n
    if end is not _sentinal:
        yield p, end 

def xrangeBy2(*args, **kw):
    return iterBy2(xrange(*args), **kw)
def rangeBy2(*args, **kw):
    return list(xrangeBy2(*args, **kw))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    assert rangeBy2(0) == []
    assert rangeBy2(0, end=None) == []
    assert rangeBy2(0, start=None) == []
    assert rangeBy2(0, start=None, end=None) == []

    assert rangeBy2(1) == []
    assert rangeBy2(1, end=None) == [(0, None)]
    assert rangeBy2(1, start=None) == [(None, 0)]
    assert rangeBy2(1, start=None, end=None) == [(None, 0), (0, None)]

    assert rangeBy2(5) == [(0, 1), (1, 2), (2, 3), (3, 4)]
    assert rangeBy2(5, end=None) == [(0, 1), (1, 2), (2, 3), (3, 4), (4, None)]
    assert rangeBy2(5, start=None) == [(None, 0), (0, 1), (1, 2), (2, 3), (3, 4)]
    assert rangeBy2(5, start=None, end=None) == [(None, 0), (0, 1), (1, 2), (2, 3), (3, 4), (4, None)]

