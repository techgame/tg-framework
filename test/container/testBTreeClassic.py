#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import unittest
from testBTree import TestBTreeData, TestBTreeDataExtensive
from TG.container import btree

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

allowLongTest = (__name__=='__main__')

class TestBTreeDataClassic(TestBTreeDataExtensive):
    BTreeFactory = btree.BTreeClassic

class TestBTreeDataClassic1024(TestBTreeDataExtensive):
    count = 1024
    BTreeFactory = btree.BTreeClassic

if allowLongTest:
    class TestBTreeDataClassic2048(TestBTreeData):
        BTreeFactory = btree.BTreeClassic
        count = 2048

    class TestBTreeDataClassic16384(TestBTreeData):
        BTreeFactory = btree.BTreeClassic
        count = 16384

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Unittest Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    unittest.main()

