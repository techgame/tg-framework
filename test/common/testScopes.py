#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import unittest
from TG.common.scopes import StackScope

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TestStackScope(unittest.TestCase):
    def test(self):
        self.A()

    def A(self):
        ss = StackScope()
        self.failUnless(ss.next() is None)
        self.assertEqual(ss.scopeVars(), {})

        ss.value = 'A'
        ss.A = "This value was set in 'A'"
        ss.fun = True

        self.B()

        self.assertEqual(ss.A, "This value was set in 'A'")
        self.assertEqual(ss.fun, True)
        self.assertEqual(ss.value, 'A')

    def B(self):
        ss = StackScope('Channel 2')
        self.failUnless(ss.next() is None)
        self.assertEqual(ss.scopeVars(), {})

        ss.B = "B decided it wanted a second channel"
        ss.icky = 1
        self.assertEqual(ss.B, "B decided it wanted a second channel")
        self.assertEqual(ss.icky, 1)

        self.C()

        self.assertEqual(ss.B, "B decided it wanted a second channel")
        self.assertEqual(ss.icky, 1)

    def C(self):
        ss = StackScope()
        self.failUnless(ss.next() is not None)
        self.assertEqual(ss.A, "This value was set in 'A'")
        self.assertEqual(ss.fun, True)
        self.assertEqual(ss.value, 'A')

        ss.value = 'C'
        ss.tricky = 3.14
        ss.C = "The method 'C' set this value"
        self.assertEqual(ss.value, 'C')
        self.assertEqual(ss.C, "The method 'C' set this value")
        self.assertEqual(ss.tricky, 3.14)

        self.D()

        self.assertEqual(ss.value, 'C')
        self.assertEqual(ss.C, "The method 'C' set this value")
        self.assertEqual(ss.tricky, 3.14)

        self.assertEqual(ss.A, "This value was set in 'A'")
        self.assertEqual(ss.fun, True)
        self.assertNotEqual(ss.value, 'A')

    def D(self):
        chNone = StackScope.forChannel()
        self.failUnless(chNone.next() is not None)
        self.assertEqual(chNone.value, 'C')
        self.assertEqual(chNone.C, "The method 'C' set this value")
        self.assertEqual(chNone.tricky, 3.14)
        self.assertEqual(chNone.A, "This value was set in 'A'")
        self.assertEqual(chNone.fun, True)
        self.assertNotEqual(chNone.value, 'A')

        ch2 = StackScope.forChannel('Channel 2')
        self.failUnless(ch2.next() is None)
        self.assertEqual(ch2.B, "B decided it wanted a second channel")
        self.assertEqual(ch2.icky, 1)

    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Unittest Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    unittest.main()


