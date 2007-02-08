#!/usr/bin/env python
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~ Copyright (C) 2002-2005  TechGame Networks, LLC.              ##
##~                                                               ##
##~ This library is free software; you can redistribute it        ##
##~ and/or modify it under the terms of the BSD style License as  ##
##~ found in the LICENSE file included with this distribution.    ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import sys
import time
from TG.algorithms import btree

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def test(BTreeClass, count, *args, **kw):
    bt = BTreeClass()
    if args:
        bt.setDegree(*args)
    debug = kw.pop('debug', False)

    if debug: print 'INSERT:'
    for x in xrange(count):
        bt[x]=x
        if debug:
            print 'bt[', x, '] =', x
            bt.printReprTree()
            print
        assert x in bt

    if debug: print 'FIND:'
    for x in xrange(count):
        assert x == bt[x], x

    if debug:
        bt.printReprTree()

    if debug: print 'DELETE:'

    for x in xrange(count):
        if debug:
            print 'del[', x,']'
        del bt[x]
        if debug:
            bt.printReprTree()
            print

        assert x not in bt, ('Should be deleted:', x)

    assert not bt, "BTree should be empty!"

def testNodeCount(BTreeClass, count, min_degree, max_degree=None):
    bt = BTreeClass()
    bt.setDegree(min_degree, max_degree)

    for x in xrange(count):
        bt[x] = x
        print x,'\r', 
        sys.stdout.flush()
    return bt

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    if 1:
        test(btree.BTree, 50, debug=True)

    if 1:
        d0 = 64; d1 = d0*8
        print
        print 'degree:', (d0, d1)
        if 1: BTreeClass = btree.BTree
        else: BTreeClass = btree.BTreeClassic
        count = 10000
        s = time.clock()
        bt = testNodeCount(BTreeClass, count, d0, d1)
        e = time.clock()
        entry = [('degree', (d0, d1)), ('time', e-s), ('items', count), ('nodes', sum(1 for n in bt.iterNodes()))]
        print entry

    if 0:
        for BTreeClass in [btree.BTreeClassic, btree.BTree]:
            for i in [1000]:
                for d in xrange(10):
                    d = 2<<d
                    print 'test:', BTreeClass, i, d
                    test(BTreeClass, i, d, debug=False)
                    print
                print

    if 0:
        table = {}
        count = 2000
        for BTreeClass in [btree.BTreeClassic, btree.BTree]:
            for b0 in xrange(2, 10):
                d0 = 1<<b0
                for b1 in xrange(b0, 11):
                    d1 = 1<<b1

                    print
                    print 'degree:', (d0, d1)
                    s = time.clock()
                    bt = testNodeCount(BTreeClass, count, d0, d1)
                    e = time.clock()

                    entry = [(d0, d1), e-s, BTreeClass, sum(1 for n in bt.iterNodes())]
                    print entry
                    table[entry[0]] = entry
                print

