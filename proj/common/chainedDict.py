#!/usr/bin/env python
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##~ Copyright (C) 2002-2004  TechGame Networks, LLC.
##~ 
##~ This library is free software; you can redistribute it and/or
##~ modify it under the terms of the BSD style License as found in the 
##~ LICENSE file included with this distribution.
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""Implements a dictionary-like with failover to a secondary dictionary-like object.

Useful for acquisition.  =)

>>> cd = ChainedDict({'testing': 1})
>>> cd.SetChained({'testing': 21, 'chained': 42})
{'testing': 21, 'chained': 42}
>>> cd.source
{'testing': 1}
>>> cd.chained
{'testing': 21, 'chained': 42}
>>> cd.items()
[('testing', 1)]
>>> cd.items(include_chained=1)
[('testing', 1), ('chained', 42)]
>>> cd['testing'] == 1
1
>>> cd['chained'] == 42
1
>>> del cd['testing']
>>> cd['testing'] == 21
1
>>> cd['testing'] = 37
>>> cd.items(include_chained=1)
[('testing', 37), ('chained', 42)]
>>> cd.items()
[('testing', 37)]
>>> cd['testing'] == 37
1
>>> cd.get('testing', None) == 37
1
>>> del cd['testing']
>>> cd['testing'] == 21
1
>>> 'testing' in cd
1
>>> 'chained' in cd
1
>>> 'not_there' not in cd
1
>>> cd.get('testing', None) == 21
1
>>> cd.get('chained', None) == 42
1
>>> cd.items()
[]
>>> cd.items(include_chained=1)
[('testing', 21), ('chained', 42)]
"""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ChainedDict(object):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def SetChained(self, chained):
        self.chained = chained or {}
        return self.chained
        
    def GetChained(self):
        return self.chained

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Dictonary Compatability
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __init__(self, data=None, chained=None):
        self.source = data or {}
        self.chained = chained or {}

    def __repr__(self):
        return "%s(%r, %r)" % (self.__class__.__name__, self.source, self.chained)

    def __eq__(self, other): 
        return self.source == other.source and self.chained == other.chained
    def __ne__(self, other):
        return self.source != other.source and self.chained != other.chained
    def __lt__(self, other):
        return self.source < other.source and self.chained < other.chained
    def __le__(self, other):
        return self.source <= other.source and self.chained <= other.chained
    def __gt__(self, other):
        return self.source > other.source and self.chained > other.chained
    def __ge__(self, other):
        return self.source >= other.source and self.chained >= other.chained

    def __len__(self, include_chained=True):
        if include_chained:
            return len(self.keys(True))
        else:
            return len(self.source)

    def __contains__(self, obj): 
        return self.source.__contains__(obj) or self.chained.__contains__(obj)
    
    def __getitem__(self, key):
        if key in self.source:
            return self.source[key]
        else:
            return self.chained[key]

    def __setitem__(self, *args, **kw): 
        return self.source.__setitem__(*args, **kw)

    def __delitem__(self, name):
        if self.source.__contains__(name):
            return self.source.__delitem__(name)

    def copy(self): 
        result = self.source.copy()
        result.update(self.chained)
        return result

    def get(self, key, *args): 
        if key in self.source:
            return self.source[key]
        else:
            return self.chained.get(key, *args)

    def clear(self, *args, **kw): 
        return self.source.clear(*args, **kw)
    
    def update(self, *args, **kw): 
        return self.source.update(*args, **kw)

    def has_key(self, *args, **kw): 
        return self.source.has_key(*args, **kw) or self.chained.has_key(*args, **kw)

    def setdefault(self, name, default):
        if name not in self:
            return self.source.setdefault(name, default)
        else:
            return self.get(name)

    def __not_contains(self, obj):
        return not self.source.__contains__(obj)

    def keys(self, include_chained=0): 
        if include_chained:
            chainedkeys = filter(self.__not_contains, self.chained)
            return self.source.keys() + chainedkeys
        else:
            return self.source.keys()

    def values(self, include_chained=0): 
        if include_chained:
            chainedkeys = filter(self.__not_contains, self.chained)
            chainedvalues = map(self.chained.get, chainedkeys)
            return self.source.values() + chainedvalues 
        else:
            return self.source.values()

    def items(self, include_chained=0): 
        if include_chained:
            chainedkeys = filter(self.__not_contains, self.chained)
            chainedvalues = map(self.chained.get, chainedkeys)
            return self.source.items() + zip(chainedkeys, chainedvalues)
        else:
            return self.source.items()

    def iterkeys(self, include_chained=0): 
        if include_chained:
            return iter(self.keys())
        else:
            return self.source.iterkeys()

    def itervalues(self, include_chained=0): 
        if include_chained:
            return iter(self.values())
        else:
            return self.source.itervalues()

    def iteritems(self, include_chained=0): 
        if include_chained:
            return iter(self.items())
        else:
            return self.source.iteritems()

    def __iter__(self): 
        return self.iterkeys()

    def __hash__(self):
        return self.source.__hash__()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class DictCollection(object):
    """Makes a list of dicts act like a single dict.  
    Any modifications only happen to the first entry.
    
    """

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Special 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __init__(self, *args):
        self.collection = self.collectionFactory(args)

    def __repr__(self): 
        return "%s(*%r)" % (self.__class__.__name__, repr(self.collection))

    def __eq__(self, other):
        return self.collection.__eq__(other.collection)
    def __ne__(self, other):
        return self.collection.__ne__(other.collection)
    def __lt__(self, other):
        return self.collection.__lt__(other.collection)
    def __le__(self, other):
        return self.collection.__le__(other.collection)
    def __gt__(self, other):
        return self.collection.__gt__(other.collection)
    def __ge__(self, other):
        return self.collection.__ge__(other.collection)

    def __iter__(self): 
        return self.iterkeys()

    def __len__(self, all=True):
        if all:
            return len(self.copy())
        else:
            return len(self._defaultdict())

    def __contains__(self, obj):
        for each in self.collection:
            if obj in each:
                return True
        return False

    def __getitem__(self, key):
        for each in self.collection:
            try:
                return each[key]
            except KeyError: 
                continue
        raise KeyError, key

    def __setitem__(self, name, value): 
        return self._defaultdict().__setitem__(name, value)

    def __delitem__(self, name):
        return self._defaultdict().__delitem__(name)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def get(self, key, default=None): 
        try:
            self.__getitem__(key)
        except KeyError:
            return default

    def update(self, *args, **kw): 
        return self._defaultdict().update(*args, **kw)

    def has_key(self, key): 
        for each in self.collection:
            if each.has_key(key):
                return True
        return False

    def setdefault(self, name, default):
        try:
            self.__getitem__(key)
        except KeyError:
            return self._defaultdict().setdefault(name, default)

    def clear(self):
        self.collection = self.collectionFactory()
    
    def copy(self): 
        collection = list(self.collection)[:]
        collection.reverse()
        result = {}
        map(result.update, collection)
        return result

    def keys(self, all=True): 
        if all:
            return self.copy().keys()
        else:
            return self._defaultdict().keys()

    def values(self, all=True): 
        if all:
            return self.copy().values()
        else:
            return self._defaultdict().values()

    def items(self, all=True): 
        if all:
            return self.copy().items()
        else:
            return self._defaultdict().items()

    def iterkeys(self, all=True): 
        return iter(self.keys(all))

    def itervalues(self, all=True): 
        return iter(self.values(all))

    def iteritems(self, all=True): 
        return iter(self.items(all))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Protected Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def collectionFactory(self):
        return list()

    def _defaultdict(self):
        # this should just return the equivalent of collection[0], without the getitem
        for each in self.collection:
            return each 
        else:
            # or create the default on the fly
            result = {}
            self.collection = self.collectionFactory([result])
            return result

ChainedDictCollection = DictCollection

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Testing 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    print "Testing..."
    print 

    import doctest, chainedDict as TestModule
    doctest.testmod(TestModule)

    cd = ChainedDict({'testing': 1})
    cd.SetChained({'testing': 21, 'chained': 42})

    print cd
    print cd.source
    print cd.chained
    print

    print cd.items()
    print cd.items(include_chained=1)
    print
    assert cd['testing'] == 1
    assert cd['chained'] == 42
    del cd['testing']
    assert cd['testing'] == 21
    cd['testing'] = 37

    print cd.items(include_chained=1)
    print cd.items()
    print

    assert cd['testing'] == 37
    assert cd.get('testing', None) == 37
    del cd['testing']
    assert cd['testing'] == 21

    assert 'testing' in cd
    assert 'chained' in cd
    assert 'not_there' not in cd

    assert cd.get('testing', None) == 21
    assert cd.get('chained', None) == 42

    print cd.items()
    print cd.items(include_chained=1)
    print

    print "Test complete."


