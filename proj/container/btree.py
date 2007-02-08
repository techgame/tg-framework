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
from btreeBase import BTreeBasic
from btreeMixin import BTreeDictMixin
import btreeNodes

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class LeafNode(btreeNodes.BTreeLeafNode): 
    __slots__ = btreeNodes.BTreeLeafNode.__slots__
class DictLeafNode(btreeNodes.BTreeDictLeafNode):
    __slots__ = btreeNodes.BTreeDictLeafNode.__slots__
class BranchNode(btreeNodes.BTreeBranchNode):
    __slots__ = btreeNodes.BTreeBranchNode.__slots__

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class BTreeFoundation(BTreeDictMixin, BTreeBasic):
    LeafFactory = None
    BranchFactory = None

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def iterWalk(self):
        return self._getRootNode().iterWalk()
    def iterNodes(self, level=None):
        return self._getRootNode().iterAllNodes(level)

    def printReprTree(self, out=None, sep='', indent='    '):
        if out is None:
            out = sys.stdout

        print >> out, repr(self)
        for level, node in self.iterNodes(1):
            print >> out, '%s%s%r' % (indent*level, sep, node)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Degree and KeyCmp methods
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getDegree(self):
        return self.minDegree, self.maxDegree
    def setDegree(self, minDegree, maxDegree=None):
        if isinstance(minDegree, tuple):
            if len(minDegree) > 1:
                minDegree, maxDegree = minDegree
            else:
                minDegree, = minDegree
        minDegree = max(2, minDegree)
        if maxDegree is None:
            maxDegree = 2*minDegree - 1
        else: maxDegree = max(minDegree, maxDegree)

        self.minDegree = minDegree
        self.maxDegree = maxDegree
    degree = property(getDegree, setDegree)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getKeyCmp(self):
        return self.keyCmp
    def setKeyCmp(self, keyCmp):
        if self: 
            raise Exception("Cannot change the degree on a filled Tree")
        self.keyCmp = keyCmp

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class BTreeClassic(BTreeFoundation):
    LeafFactory = LeafNode
    BranchFactory = BranchNode

class BTree(BTreeFoundation):
    LeafFactory = DictLeafNode
    BranchFactory = BranchNode

BTreeDictLeaves = BTree

