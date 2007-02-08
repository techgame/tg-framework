#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import unittest
from TG.common.iterators import rangeBy2

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TestIterBy2(unittest.TestCase):
    def testEmptyIter(self):
        self.assertEqual(rangeBy2(0), [])
        self.assertEqual(rangeBy2(0, end=None), [])
        self.assertEqual(rangeBy2(0, start=None), [])
        self.assertEqual(rangeBy2(0, start=None, end=None), [])

    def testOneElementIter(self):
        self.assertEqual(rangeBy2(1), [])
        self.assertEqual(rangeBy2(1, end=None), [(0, None)])
        self.assertEqual(rangeBy2(1, start=None), [(None, 0)])
        self.assertEqual(rangeBy2(1, start=None, end=None), [(None, 0), (0, None)])

    def testManyElementIter(self):
        self.assertEqual(rangeBy2(5), [(0, 1), (1, 2), (2, 3), (3, 4)])
        self.assertEqual(rangeBy2(5, end=None), [(0, 1), (1, 2), (2, 3), (3, 4), (4, None)])
        self.assertEqual(rangeBy2(5, start=None), [(None, 0), (0, 1), (1, 2), (2, 3), (3, 4)])
        self.assertEqual(rangeBy2(5, start=None, end=None), [(None, 0), (0, 1), (1, 2), (2, 3), (3, 4), (4, None)])

    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Unittest Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    unittest.main()

