#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import unittest
from testBTree import TestBTreeData
from TG.container import btreeN

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

count = 1024
bigCount = count * 2
hugeCount = count * 4
allowLongTest = (__name__=='__main__')

class TestBTreeDegrees4(TestBTreeData):
    count = count
    BTreeFactory = btreeN.BTree4

class TestBTreeDegrees4x16(TestBTreeData):
    count = count
    BTreeFactory = btreeN.BTree4x16

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TestBTreeDegrees16(TestBTreeData):
    count = count
    BTreeFactory = btreeN.BTree16

class TestBTreeDegrees16by64(TestBTreeData):
    count = bigCount
    BTreeFactory = btreeN.BTree16x64

if allowLongTest:
    class TestBTreeDegrees16by256(TestBTreeData):
        count = bigCount
        BTreeFactory = btreeN.BTree16x256

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TestBTreeDegrees64(TestBTreeData):
    count = count
    BTreeFactory = btreeN.BTree64

class TestBTreeDegrees64by256(TestBTreeData):
    count = bigCount
    BTreeFactory = btreeN.BTree64x256

if allowLongTest:
    class TestBTreeDegrees64by512(TestBTreeData):
        count = bigCount
        BTreeFactory = btreeN.BTree64x512

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TestBTreeDegrees256(TestBTreeData):
    count = bigCount
    BTreeFactory = btreeN.BTree256

if allowLongTest:
    class TestBTreeDegrees256x1024(TestBTreeData):
        count = hugeCount
        BTreeFactory = btreeN.BTree256x1024

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Unittest Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    unittest.main()

