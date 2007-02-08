#!/usr/bin/env python
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##~ Copyright (C) 2002-2004  TechGame Networks, LLC.
##~ 
##~ This library is free software; you can redistribute it and/or
##~ modify it under the terms of the BSD style License as found in the 
##~ LICENSE file included with this distribution.
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class AttributedDict(dict):
    """AttributedDict is intended to be a handly little class that you can
    stuff attributes and such into like you would any other class, yet have
    the nice iteration capabilities of a dictionary.
    
    >>> test = AttributedDict()
    >>> test.fun
    Traceback (most recent call last):
    AttributeError: 'AttributedDict' object has no attribute 'fun'
    >>> test.fun = 7
    >>> test.fun
    7
    >>> test.items()
    [('fun', 7)]
    >>> test.more = test.fun * 3
    >>> test
    {'fun': 7, 'more': 21}
    >>> testupdate = {'regular':'dict'}
    >>> testupdate.update(test)
    >>> testupdate
    {'fun': 7, 'regular': 'dict', 'more': 21}
    >>> test.more
    21
    >>> test.regular
    Traceback (most recent call last):
    AttributeError: 'AttributedDict' object has no attribute 'regular'
    >>> test.update(testupdate)
    >>> test.regular
    'dict'
    >>> test
    {'fun': 7, 'regular': 'dict', 'more': 21}

    """
    
    __slots__ = ()

    def __getattribute__(self, name):
        """Allows access to "attributes" by either obj.name, or obj[name]"""
        try:
            return dict.__getattribute__(self, name)
        except AttributeError:
            if name in self:
                return self[name]
            else: raise

    def __setattr__(self, name, value):
        """Allows setting "attributes" by obj.name = value, or obj[name] = value"""
        try:
            dict.__setattr__(self, name, value)
        except AttributeError:
            self[name] = value

    def __delattr__(self, name):
        """Allows deleteing of "attributes" by del obj.name  or del obj[name]"""
        try:
            dict.__delattr__(self, name)
        except AttributeError:
            if name in self:
                del self[name]
            else: raise

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Testing 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    print "Testing..."

    class _test(AttributedDict): 
        answer = 42

    d = _test()

    # Test write
    d.test = 'working'

    # Test read
    assert 'working' == d.test
    assert 42 == d.answer
    assert 'answer' not in d

    # Test delete
    del d.test
    assert not hasattr(d, 'test')

    try:
        # Test reading the now deleted attribute
        d.test == 'this shouldnt really work'
        assert 0
    except AttributeError:
        pass

    try:
        # Test deleting an attribute that wasnt there in the first place...
        del d.ThiSneverExisted
        assert 0
    except AttributeError:
        pass

    import time
    class Normal(object):
        answer = 42**2
    normal = Normal()
    count = 1000
    start = time.clock()
    for i in xrange(count): me = i + normal.answer
    pereach = (time.clock() - start) / count
    print "Normal:", pereach, "per", count

    start = time.clock()
    for i in xrange(count): me = i + d.answer
    pereach2 = (time.clock() - start) / count
    print "Attributed Dict:", pereach2, "per", count

    print "Attributed Dict is", pereach2/pereach, "times slower" 

    print 
    print 

    import doctest, attributedDict
    doctest.testmod(attributedDict)

    print "Test complete."
