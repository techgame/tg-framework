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

from TG.common.iterators import iterBy2

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class BTreeBase(object):
    def isBTree(self):
        return True

    @staticmethod
    def objIsBtree(obj):
        if hasattr(obj, 'isBTree'):
            return obj.isBTree()
        else: return False

    def _find(self, key):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def _insert(self, key, value):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def _delete(self, key):
        self._pop(key)
    def _pop(self, key, *args):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class BTreeBasic(BTreeBase):
    LeafFactory = None
    BranchFactory = None

    minDegree = 2
    maxDegree = minDegree*2-1
    keyCmp = staticmethod(cmp)

    def __init__(self):
        self._newRootNode()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Interface
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _treeCtx(self):
        return self

    def _find(self, key, *args):
        node, item, idx = self._findHostOfKey(key)
        if item is None:
            if args: return args[0]
            raise KeyError(key)
        treeCtx = self._treeCtx()
        result = node.findItem(treeCtx, key, item, idx, *args)
        return result

    def _insert(self, key, value):
        stack = self._nodeStackFor(key, True)
        idx = stack[0][1]
        treeCtx = self._treeCtx()
        result = stack[1].insertItem(treeCtx, key, (key, value), idx)
        self._splitFullStackNodes(stack[1:])

    def _delete(self, key):
        self._pop(key)

    def _pop(self, key, *args):
        stack = self._nodeStackFor(key, True)
        item, idx = stack[0]
        treeCtx = self._treeCtx()
        result = stack[1].popItem(treeCtx, key, item, idx, *args)
        self._balanceStackNodes(stack[1:])
        return result

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Root Storage
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    _rootNode = None
    def _getRootNode(self):
        return self._rootNode
    def _setRootNode(self, rootNode):
        self._rootNode = rootNode
    def _newRootNode(self):
        self._setRootNode(self.LeafFactory())

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Tools
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _findHostOfKey(self, key):
        treeCtx = self._treeCtx()
        node = self._getRootNode()
        while node is not None:
            node, item, hint = node.findHostOfKey(treeCtx, key)
            if item is not None:
                return (node, item, hint)
        else:
            return (node, None, None)

    def _iterNodeTrace(self, key, incItem=False):
        treeCtx = self._treeCtx()
        node, item, idx = self._getRootNode(), None, None
        while node is not None:
            yield node
            node, item, idx = node.findHostOfKey(treeCtx, key)
            if item is not None:
                break
        if incItem:
            yield item, idx

    def _nodeStackFor(self, key, incItem=False):
        result = list(self._iterNodeTrace(key, incItem))
        result.reverse()
        return result

    def _insertSplitNode(self, leftNode, midItem, rightNode):
        rootNode = self.BranchFactory.fromBranch(leftNode, midItem, rightNode)
        self._setRootNode(rootNode)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Adjustment tools
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _splitFullStackNodes(self, stack):
        treeCtx = self._treeCtx()
        for node, parentNode in iterBy2(stack, end=self):
            if not node.split(treeCtx, parentNode):
                break

    def _balanceStackNodes(self, stack):
        treeCtx = self._treeCtx()
        for node, parentNode in iterBy2(stack, end=self):
            if not node.balance(treeCtx, parentNode):
                break

    def _getPeerNodesOf(self, node):
        return 0, None, None

    def _collapseChild(self, child):
        if child:
            return False

        nodes = child.getNodes()
        if len(nodes) != 1:
            return False

        self._setRootNode(nodes[0])
        return True

