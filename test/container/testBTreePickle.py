#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import unittest
import pickle
import cPickle
from TG.container import btree
from TG.container import btreeN

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

allowLongTest = (__name__=='__main__')

class TestBTreePickle(unittest.TestCase):
    BTreeFactory = btree.BTree
    compareFactor = {0: 3.1, 1: 4.5, 2: 3.4}

    DEBUG = False

    count = 1000
    data = None
    def initData(klass):
        if klass.data is not None:
            if len(klass.data) == klass.count:
                return klass.data
        klass.data = dict([(x,x) for x in xrange(klass.count)])
        klass.pickleLen = {
            0: len(pickle.dumps(klass.data, 0)),
            1: len(pickle.dumps(klass.data, 1)),
            2: len(pickle.dumps(klass.data, 2)),
            }
        return klass.data
    initData = classmethod(initData)

    def setUp(self):
        self.initData()
        self.bt = self.BTreeFactory(self.data)

    def tearDown(self):
        del self.bt

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _doPickleCompare(self, dumps, protocol):
        pbt = len(dumps(self.bt, protocol))
        d = self.pickleLen[protocol]
        f = self.compareFactor[protocol]

        if self.DEBUG:
            print
            print protocol, self.bt.degree, len(list(self.bt.iterNodes()))
            print '    %d %d' % (d, pbt)
            print '    %d %d %d' % (pbt, d*f, d*f-pbt)
            print '    %1.2f %1.2f' % (pbt/float(d), f)

        self.failUnlessEqual(sorted(self.data.items()), sorted(self.bt.items()))
        self.failUnless(d < pbt)
        self.failUnless(pbt < (d * f))

    def testPickle0(self):
        self._doPickleCompare(pickle.dumps, 0)
    def testPickle1(self):
        self._doPickleCompare(pickle.dumps, 1)
    def testPickle2(self):
        self._doPickleCompare(pickle.dumps, 2)
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testCPickle0(self):
        self._doPickleCompare(cPickle.dumps, 0)
    def testCPickle1(self):
        self._doPickleCompare(cPickle.dumps, 1)
    def testCPickle2(self):
        self._doPickleCompare(cPickle.dumps, 2)
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TestBTreePickleClassic(TestBTreePickle):
    BTreeFactory = btree.BTreeClassic
    compareFactor = {0: 3.6, 1: 5.3, 2: 4.1}

class TestBTreePickle64(TestBTreePickle):
    BTreeFactory = btreeN.BTree64
    compareFactor = {0: 1.08, 1: 1.11, 2: 1.07}

class TestBTreePickle256(TestBTreePickle):
    BTreeFactory = btreeN.BTree256
    compareFactor = {0: 1.04, 1: 1.06, 2: 1.04}

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Unittest Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    unittest.main()
    print 'Total Items:', TestBTreePickle.totalItems

