#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import unittest
from TG.container import btree

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

allowLongTest = (__name__=='__main__')

class TestBTreeData(unittest.TestCase):
    BTreeFactory = btree.BTree
    count = 64

    data = None
    def initData(klass):
        if klass.data is not None:
            if len(klass.data) == klass.count:
                return klass.data
        klass.data = [(x,x) for x in xrange(klass.count)]
        return klass.data
    initData = classmethod(initData)

    def setUp(self):
        self.initData()
        self.bt = self.BTreeFactory(self.data)

    def tearDown(self):
        del self.bt

    def testContains(self):
        bt = self.bt
        for k,v in self.data:
            self.failUnless(k in bt)

    def testGet(self):
        bt = self.bt
        for k,v in self.data:
            self.assertEqual(bt[k], v)
    
    def testPopPattern1(self):
        bt = self.bt
        for k,v in self.data:
            self.assertEqual(bt.pop(k), v)

class TestBTreeDataExtensive(TestBTreeData):
    def testPopPattern2(self):
        bt = self.bt
        for k,v in self.data[::2]:
            self.assertEqual(bt.pop(k), v)
        for k,v in self.data[1::2]:
            self.assertEqual(bt.pop(k), v)

        self.failIf(bool(bt), "BTree should be empty")
    
    def testPopPattern3(self):
        bt = self.bt
        for k,v in self.data[::3]:
            self.assertEqual(bt.pop(k), v)
        for k,v in self.data[2::3]:
            self.assertEqual(bt.pop(k), v)
        for k,v in self.data[1::3]:
            self.assertEqual(bt.pop(k), v)

        self.failIf(bool(bt), "BTree should be empty")
    
    def testDelPattern1(self):
        bt = self.bt
        for k,v in self.data:
            self.failUnless(k in bt)
            del bt[k]
            self.failIf(k in bt)

        self.failIf(bool(bt), "BTree should be empty")
    
    def testDelPattern2(self):
        bt = self.bt
        for k,v in self.data[1::2]:
            self.failUnless(k in bt)
            del bt[k]
            self.failIf(k in bt)

        for k,v in self.data[::2]:
            self.failUnless(k in bt)
            del bt[k]
            self.failIf(k in bt)

        self.failIf(bool(bt), "BTree should be empty")
    
    def testDelPattern3(self):
        bt = self.bt
        for k,v in self.data[2::3]:
            self.failUnless(k in bt)
            del bt[k]
            self.failIf(k in bt)

        for k,v in self.data[::3]:
            self.failUnless(k in bt)
            del bt[k]
            self.failIf(k in bt)

        for k,v in self.data[1::3]:
            self.failUnless(k in bt)
            del bt[k]
            self.failIf(k in bt)

        self.failIf(bool(bt), "BTree should be empty")
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TestBTreeData1024(TestBTreeDataExtensive):
    count = 1024

if 0 and allowLongTest:
    class TestBTreeData2048(TestBTreeData):
        count = 2048

    class TestBTreeData16384(TestBTreeData):
        count = 16384

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Unittest Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    unittest.main()

