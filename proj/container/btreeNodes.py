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

from itertools import izip

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class BTreeNodeBase(object):
    __slots__ = ['_items']

    def __init__(self):
        self._initNode()

    def __getstate__(self):
        return self._items
    def __setstate__(self, state):
        self._items = state

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Storage
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _initNode(self):
        self.setItems()

    def __repr__(self):
        return '<%s.%s %s>' % (
                self.__class__.__module__, 
                self.__class__.__name__,
                self.reprItems())

    def reprItems(self):
        return '{' + ', '.join('%r: %r' % i for i in self.getItems()) + '}'

    def __len__(self):
        return len(self.getItems())

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Item and iteration methods
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    _items = None
    def getItems(self):
        return self._items
    def setItems(self, items=None):
        if items is None:
            items = []
        self._items = items
    def iterItems(self):
        return iter(self.getItems())

    def getNodes(self):
        return ()
    def iterNodes(self):
        return iter(self.getNodes())

    def iterAllNodes(self, level=None):
        if level is None:
            stack = [self]
            while stack:
                node = stack.pop()
                stack.extend(reversed(node.getNodes()))
                yield node
        else:
            stack = [(level, self)]
            while stack:
                i, node = stack.pop()
                stack.extend((i+1, n) for n in reversed(node.getNodes()))
                yield i, node

    def getNodeAtIdx(self, idx):
        if self.isLeaf():
            return None
        else: return self.getNodes()[idx]

    def isLeaf(self): 
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Interface
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def iterWalk(self):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def iteritems(self):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

    def findItem(self, treeCtx, key, hintItem, idx=None, *args):
        # This one is sort of retorical -- hintItem is passed
        # from the result of findHostOfKey's residual hintItem.
        # We just echo it here for effeciency while
        # maintaining encapsulation
        if hintItem is None:
            if args: return args[0]
            raise KeyError(key)
        return hintItem

    def insertItem(self, treeCtx, key, item, idx=None):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

    def popItem(self, treeCtx, key, hintItem, idx=None, *args):
        # Item is passed from the result of findHostOfKey's residual hintItem.
        if not hintItem:
            if args: return args[0]
            raise KeyError(key)

        if idx is None:
            idx = self.getItems().index(hintItem)
        self._removeIndex(treeCtx, idx)
        return hintItem[1]

    def _removeIndex(self, treeCtx, idx):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Key Tools 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def findHostOfKey(self, treeCtx, key):
        idx, itemAtKey = self._idxInfoFromKey(treeCtx, key)
        if itemAtKey:
            return self, itemAtKey, idx
        else:
            return self.getNodeAtIdx(idx), None, idx

    def _idxInfoFromIdxOrKey(self, treeCtx, idx, key, default=(), end=()):
        if idx is None:
            idx, itemAtKey = self._idxInfoFromKey(treeCtx, key)
        else:
            items = self.getItems()
            if idx < len(items):
                itemAtKey = items[idx]
                if 0 != treeCtx.keyCmp(itemAtKey[0], key):
                    itemAtKey = None
            else: 
                itemAtKey = None
        return idx, itemAtKey

    def _idxInfoFromKey(self, treeCtx, key, default=(), end=()):
        idx = -1
        keyCmp = treeCtx.keyCmp
        for idx, (iKey, iValue) in enumerate(self.getItems()):
            cv = keyCmp(key, iKey)
            if cv < 0:
                return idx, default
            elif cv == 0:
                return idx, (iKey, iValue)
        else:
            return idx+1, end

    def _swapIndex(self, idx, item):
        items = self.getItems()
        result, items[idx] = items[idx], item
        return result

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Splitting Tools
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def isUnderfilled(self, treeCtx):
        return len(self) < max(2, treeCtx.minDegree)
    def isFull(self, treeCtx):
        return len(self) > treeCtx.maxDegree

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def split(self, treeCtx, parentNode):
        if not self.isFull(treeCtx):
            return False

        midItem, nextNode = self._splitNode(treeCtx)
        parentNode._insertSplitNode(self, midItem, nextNode)
        return True

    def _splitNode(self, treeCtx):
        pivotItem, splitItems = self._splitChildren(treeCtx)
        nextNode = self._newFromSplitItems(treeCtx, splitItems)
        return pivotItem, nextNode

    def _splitChildren(self, treeCtx):
        items, nodes = self.getItems(), self.getNodes()
        idx = len(items)//2
        pivotItem = items[idx]
        splitItems = (items[idx+1:], nodes[idx+1:])

        del items[idx:]
        if nodes:
            del nodes[idx+1:]
        return pivotItem, splitItems

    def _newFromSplitItems(self, treeCtx, items):
        return self.fromSplit(items)

    @classmethod
    def fromSplit(klass, (items, nodes)):
        self = klass()
        self.setItems(items)
        if nodes:
            self.setNodes(nodes)
        return self

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Balancing Tools
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def balance(self, treeCtx, parentNode):
        if not self.isUnderfilled(treeCtx):
            return False
        return self._balanceNode(treeCtx, parentNode)

    def _balanceNode(self, treeCtx, parentNode):
        idx, prevNode, nextNode = parentNode._getPeerNodesOf(self)

        if prevNode is None:
            if nextNode is None:
                parentNode._collapseChild(self)

            elif nextNode.isUnderfilled(treeCtx):
                # combine self with next node
                parentNode._combineIndex(treeCtx, idx)
            else:
                # shift min item from nextNode to parent, and from parent to self
                parentNode._rotateItemDown(treeCtx, idx, self, nextNode)
        elif prevNode.isUnderfilled(treeCtx):
            # combine prev node with self
            parentNode._combineIndex(treeCtx, idx-1)
        else:
            # shift max item from prevNode to parent, and from parent to self
            parentNode._rotateItemUp(treeCtx, idx-1, prevNode, self)

        return True

    def combineWith(self, item, next):
        items = self.getItems()
        if item is not None:
            items.append(item)
        items.extend(next.getItems())

        nodes = next.getNodes()
        if nodes:
            self.getNodes().extend(nodes)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Min/Maxes
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def minNode(self):
        return self.getNodeAtIdx(0)
    def maxNode(self):
        return self.getNodeAtIdx(-1)

    def findMinLeafNode(self):
        node, next = self, self.minNode()
        while next is not None:
            node, next = next, node.minNode()
        return node

    def findMaxLeafNode(self):
        node, next = self, self.maxNode()
        while next is not None:
            node, next = next, node.maxNode()
        return node

    def _popMinLeafItem(self, treeCtx):
        node = self.findMinLeafNode()
        node, item = node._popMinEntry(treeCtx)
        assert node is None
        return item
    def _popMaxLeafItem(self, treeCtx):
        node = self.findMaxLeafNode()
        node, item = node._popMaxEntry(treeCtx)
        assert node is None
        return item

    def _pushMinEntry(self, node, item):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def _popMinEntry(self, treeCtx):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def _pushMaxEntry(self, node, item):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def _popMaxEntry(self, treeCtx):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Branch Node Base
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class BTreeBranchNodeBase(BTreeNodeBase):
    __slots__ = BTreeNodeBase.__slots__ + ['_nodes']

    def __getstate__(self):
        return self._items, self._nodes
    def __setstate__(self, state):
        self._items, self._nodes = state

    def _initNode(self):
        BTreeNodeBase._initNode(self)
        self.setNodes()

    _nodes = None
    def getNodes(self):
        return self._nodes
    def setNodes(self, nodes=None):
        if nodes is None:
            nodes = []
        self._nodes = nodes

    def getNodeAtIdx(self, idx):
        return self.getNodes()[idx]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def isLeaf(self):
        return False

    @classmethod
    def fromBranch(klass, leftNode, midItem, rightNode):
        return klass.fromSplit(([midItem], [leftNode, rightNode]))

    def _collapseChild(self, node):
        assert type(self) is type(node)
        assert not self and len(self.getNodes()) == 1
        self.setItems(node.getItems())
        self.setNodes(node.getNodes())
        return True

    def _pushMinEntry(self, node, item):
        items, nodes = self.getItems(), self.getNodes()
        items.insert(0, item)
        if node is not None:
            nodes.insert(0, node)
    def _popMinEntry(self, treeCtx):
        items, nodes = self.getItems(), self.getNodes()
        if nodes:
            return nodes.pop(0), items.pop(0)
        else: return None, items.pop(0)
    def _pushMaxEntry(self, node, item):
        items, nodes = self.getItems(), self.getNodes()
        items.append(item)
        if node is not None:
            nodes.append(node)
    def _popMaxEntry(self, treeCtx):
        items, nodes = self.getItems(), self.getNodes()
        if nodes:
            return nodes.pop(), items.pop()
        else: return None, items.pop()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _getPeerNodesOf(self, node):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def _insertSplitNode(self, leftNode, midItem, rightNode):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def _combineIndex(self, treeCtx, idx):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def _rotateItemUp(self, treeCtx, idx, node, nextNode):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def _rotateItemDown(self, treeCtx, idx, node, nextNode):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class BTreeBranchNode(BTreeBranchNodeBase):
    __slots__ = BTreeBranchNodeBase.__slots__

    def iterWalk(self):
        inodes = self.iterNodes()
        for node, i in izip(inodes, self.getItems()):
            yield False, node
            yield True, i

        for node in inodes:
            yield False, node

    def iteritems(self):
        inodes = self.iterNodes()
        for i, node in izip(self.getItems(), inodes):
            for ni in node.iteritems():
                yield ni
            yield i
        for node in inodes:
            for ni in node.iteritems():
                yield ni

    def insertItem(self, treeCtx, key, item, idx=None):
        items = self.getItems()
        idx, itemAtKey = self._idxInfoFromIdxOrKey(treeCtx, idx, key)
        if not itemAtKey:
            raise RuntimeError("Insert item should not be called on an interior node that does not hold the key")

        items[idx] = item

    def _removeIndex(self, treeCtx, idx):
        items, nodes = self.getItems(), self.getNodes()
        if not nodes:
            # this happens at the root node
            items.pop(idx)

        else:
            prevNode, nextNode = nodes[idx:idx+2]

            if not prevNode.isUnderfilled(treeCtx):
                # steal from lower node
                items[idx] = prevNode._popMaxLeafItem(treeCtx)
            elif not nextNode.isUnderfilled(treeCtx):
                # steal from greater node
                items[idx] = nextNode._popMinLeafItem(treeCtx)
            else:
                # both nodes can be combined
                items[idx] = None
                self._combineIndex(treeCtx, idx)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _getPeerNodesOf(self, node):
        nodes = self.getNodes()
        nodeIdx = nodes.index(node)
        if nodeIdx: 
            prev = nodes[nodeIdx-1]
        else: prev = None

        if nodeIdx < len(nodes)-1: 
            next = nodes[nodeIdx+1]
        else: next = None
        return nodeIdx, prev, next

    def _insertSplitNode(self, leftNode, midItem, rightNode):
        items, nodes = self.getItems(), self.getNodes()
        idx = nodes.index(leftNode)
        items.insert(idx, midItem)
        nodes.insert(idx+1, rightNode)

    def _combineIndex(self, treeCtx, idx):
        items, nodes = self.getItems(), self.getNodes()
        node = nodes[idx]
        item = items.pop(idx)
        nextNode = nodes.pop(idx+1)
        node.combineWith(item, nextNode)
        return node

    def _rotateItemUp(self, treeCtx, idx, node, nextNode):
        # shift max item from prevNode to parent, and from parent to self
        maxNode, maxItem = node._popMaxEntry(treeCtx)
        itemAtIdx = self._swapIndex(idx, maxItem)
        nextNode._pushMinEntry(maxNode, itemAtIdx)

    def _rotateItemDown(self, treeCtx, idx, node, nextNode):
        # shift min item from nextNode to parent, and from parent to self
        minNode, minItem = nextNode._popMinEntry(treeCtx)
        itemAtIdx = self._swapIndex(idx, minItem)
        node._pushMaxEntry(minNode, itemAtIdx)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Leaf Node Base
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class BTreeLeafNodeBase(BTreeNodeBase):
    __slots__ = BTreeNodeBase.__slots__

    def isLeaf(self):
        return True

    def getNodeAtIdx(self, idx):
        return None

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def iterWalk(self):
        return ((True, e) for e in self.iterItems())
    def iteritems(self):
        return self.iterItems()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _popMinLeafItem(self, treeCtx):
        return self._popMinEntry(treeCtx)[1]
    def _popMaxLeafItem(self, treeCtx):
        return self._popMaxEntry(treeCtx)[1]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class BTreeLeafNode(BTreeLeafNodeBase):
    __slots__ = BTreeLeafNodeBase.__slots__

    def insertItem(self, treeCtx, key, item, idx=None):
        items = self.getItems()
        idx, itemAtKey = self._idxInfoFromIdxOrKey(treeCtx, idx, key)

        if itemAtKey:
            items[idx] = item
        else:
            items.insert(idx, item)

    def _removeIndex(self, treeCtx, idx):
        items = self.getItems()
        items.pop(idx)

    def _pushMinEntry(self, node, item):
        assert node is None
        self.getItems().insert(0, item)
    def _popMinEntry(self, treeCtx):
        return (None, self.getItems().pop(0))

    def _pushMaxEntry(self, node, item):
        assert node is None
        self.getItems().append(item)
    def _popMaxEntry(self, treeCtx):
        return (None, self.getItems().pop(-1))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class BTreeDictLeafNode(BTreeLeafNodeBase):
    __slots__ = BTreeLeafNodeBase.__slots__

    def getItems(self):
        return self.getItemsDict().iteritems()
    def setItems(self, items=None):
        if items is None:
            return self.setItemsDict(dict())
        itemsDict = self.getItemsDict()
        itemsDict.clear()
        itemsDict.update(items)
    def iterItems(self):
        return self.getItemsDict().iteritems()

    def __len__(self):
        return len(self.getItemsDict())
    def getItemsDict(self):
        return self._items
    def setItemsDict(self, items=None):
        self._items = items

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _idxInfoFromKey(self, treeCtx, key, default=(), end=()):
        raise NotImplementedError("Invalid method for this subclass")
    def _idxInfoFromIdxOrKey(self, treeCtx, idx, key, default=(), end=()):
        raise NotImplementedError("Invalid method for this subclass")

    def findHostOfKey(self, treeCtx, key):
        itemDict = self.getItemsDict()
        try:
            return self, (key, itemDict[key]), None
        except LookupError:
            return None, None, None

    def combineWith(self, item, next):
        itemsDict = self.getItemsDict()
        if item is not None:
            itemsDict[item[0]] = item[1]
        itemsDict.update(next.getItems())

    def insertItem(self, treeCtx, key, item, idx=None):
        self.getItemsDict()[item[0]] = item[1]

    def popItem(self, treeCtx, key, hintItem, idx=None, *args):
        value = self.getItemsDict().pop(key, *args)
        return value

    def _removeIndex(self, treeCtx, idx):
        raise NotImplementedError("Invalid method for this subclass")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _splitChildren(self, treeCtx):
        itemsDict = self.getItemsDict()
        splitKeys = itemsDict.keys()
        splitKeys.sort(cmp=treeCtx.keyCmp)
        idx = len(splitKeys)//2
        pivotKey = splitKeys[idx]
        splitKeys = splitKeys[idx+1:]

        pivotItem = (pivotKey, itemsDict.pop(pivotKey))
        splitItemsDict = dict((k, itemsDict.pop(k)) for k in splitKeys)
        return pivotItem, (splitItemsDict, [])

    def getItemsSorted(self, splitItems=None, keyCmp=cmp):
        if splitItems is None:
            splitItems = self.getItemsDict().items()

        def itemCmp(i0, i1):
            return keyCmp(i0[0], i1[0])
        splitItems.sort(cmp=itemCmp)
        return splitItems

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _pushMinEntry(self, node, item):
        assert node is None
        self.getItemsDict()[item[0]] = item[1]
    def _popMinEntry(self, treeCtx):
        itemsDict = self.getItemsDict()

        iItems = itemsDict.iteritems()
        popKey = iItems.next()[0]
        keyCmp = treeCtx.keyCmp
        for k,v in iItems:
            if keyCmp(popKey, k) > 0:
                popKey = k

        result = itemsDict.pop(popKey)
        return (None, (popKey, result))

    def _pushMaxEntry(self, node, item):
        assert node is None
        self.getItemsDict()[item[0]] = item[1]
    def _popMaxEntry(self, treeCtx):
        itemsDict = self.getItemsDict()

        iItems = itemsDict.iteritems()
        popKey = iItems.next()[0]
        keyCmp = treeCtx.keyCmp
        for k,v in iItems:
            if keyCmp(popKey, k) < 0:
                popKey = k

        result = itemsDict.pop(popKey)
        return (None, (popKey, result))

