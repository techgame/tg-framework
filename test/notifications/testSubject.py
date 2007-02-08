#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import unittest
from TG.notifications import subject
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TestSubject(unittest.TestCase):
    def setUp(self):
        self.calledBack = False
        
    def tearDown(self):
        self.calledBack = False

    def testLambda(self):
        # this will give us a WeakList Subject, the default
        subj = subject.Subject()
        fn = lambda: setattr(self, 'calledBack', True)
        subj.add(fn)
        self.failIf(self.calledBack)
        subj.update()
        self.failUnless(self.calledBack)

    def testFunction(self):
        # this will give us a WeakList Subject, the default
        subj = subject.Subject()
        def fn():
            self.calledBack = True
        subj.add(fn)
        self.failIf(self.calledBack)
        subj.update()
        self.failUnless(self.calledBack)

    def fn(self, *args, **kw): 
        if args or kw:
            self.calledBack = args, kw
        else:
            self.calledBack = True

    def testMethod(self):
        subj = subject.Subject()
        subj.add(self.fn)
        self.failIf(self.calledBack)
        subj.update()
        self.failUnless(self.calledBack)

    def false(self):
        assert False, 'This should never get called'

    def testMethodRemove(self):
        subj = subject.Subject()
        subj.add(self.fn)
        subj.add(self.false)
        self.failIf(self.calledBack)
        subj.remove(self.false)
        subj.update()
        self.failUnless(self.calledBack)

    def testMethodWithParams(self):
        subj = subject.Subject()
        subj.add(self.fn)
        self.failIf(self.calledBack)
        subj.update(42, 'aString', floatVal=3.14)
        self.assertEqual(self.calledBack, ((42, 'aString'), {'floatVal': 3.14}))

class TestSubjectProperty(unittest.TestCase):
    class testHarness(object):
        subj = subject.SubjectProperty()

    def setUp(self):
        self.calledBack = False
        
    def tearDown(self):
        self.calledBack = False

    def fn(self, *args, **kw): 
        if args or kw:
            self.calledBack = args, kw
        else:
            self.calledBack = True

    def testMethod(self):
        obj = self.testHarness()

        prop = self.testHarness.subj
        obj.subj.add(self.fn)
        self.failIf(self.calledBack)
        obj.subj.update()
        self.failUnless(self.calledBack)

    def false(self):
        assert False, 'This should never get called'

    def testMethodRemove(self):
        obj = self.testHarness()
        obj.subj.add(self.fn)
        obj.subj.add(self.false)
        self.failIf(self.calledBack)
        obj.subj.remove(self.false)
        obj.subj.update()
        self.failUnless(self.calledBack)

    def testMethodWithParams(self):
        obj = self.testHarness()
        obj.subj.add(self.fn)
        self.failIf(self.calledBack)
        obj.subj.update(42, 'aString', floatVal=3.14)
        self.assertEqual(self.calledBack, ((42, 'aString'), {'floatVal': 3.14}))
    

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Unittest Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    unittest.main()


