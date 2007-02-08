#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import unittest
from TG.notifications import event
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TestEvent(unittest.TestCase):
    def setUp(self):
        self.calledBack = False
        
    def tearDown(self):
        self.calledBack = False

    def testLambda(self):
        # this will give us a WeakList Event, the default
        evt = event.Event()
        fn = lambda: setattr(self, 'calledBack', True)
        evt.add(fn)
        self.failIf(self.calledBack)
        evt()
        self.failUnless(self.calledBack)

    def testFunction(self):
        # this will give us a WeakList Event, the default
        evt = event.Event()
        def fn():
            self.calledBack = True
        evt.add(fn)
        self.failIf(self.calledBack)
        evt()
        self.failUnless(self.calledBack)

    def fn(self, *args, **kw): 
        if args or kw:
            self.calledBack = args, kw
        else:
            self.calledBack = True

    def testMethod(self):
        evt = event.Event()
        evt.add(self.fn)
        self.failIf(self.calledBack)
        evt()
        self.failUnless(self.calledBack)

    def false(self):
        assert False, 'This should never get called'

    def testMethodRemove(self):
        evt = event.Event()
        evt.add(self.fn)
        evt.add(self.false)
        self.failIf(self.calledBack)
        evt.remove(self.false)
        evt()
        self.failUnless(self.calledBack)

    def testMethodWithParams(self):
        evt = event.Event()
        evt.add(self.fn)
        self.failIf(self.calledBack)
        evt(42, 'aString', floatVal=3.14)
        self.assertEqual(self.calledBack, ((42, 'aString'), {'floatVal': 3.14}))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TestEventProperty(unittest.TestCase):
    class testHarness(object):
        evt = event.Event.property()
        evt1Called = False
        evt2Called = False

        def onEvent(self, *args, **kw):
            self.evt1Called = args, kw
        evt.add(onEvent)

        def onEvent2(self, *args, **kw):
            self.evt2Called = args, kw
        evt(onEvent2)


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
        obj.evt.add(self.fn)
        self.failIf(self.calledBack)
        obj.evt()
        self.failUnless(self.calledBack)

    def false(self):
        assert False, 'This should never get called'

    def testMethodRemove(self):
        obj = self.testHarness()
        obj.evt.add(self.fn)
        obj.evt.add(self.false)
        self.failIf(self.calledBack)
        self.failIf(obj.evt1Called)
        self.failIf(obj.evt2Called)
        obj.evt.remove(self.false)
        obj.evt()
        self.failUnless(self.calledBack)
        self.failUnless(obj.evt1Called)
        self.failUnless(obj.evt2Called)

    def testMethodWithParams(self):
        obj = self.testHarness()
        obj.evt.add(self.fn)
        self.failIf(self.calledBack)
        self.failIf(obj.evt1Called)
        self.failIf(obj.evt2Called)
        obj.evt(42, 'aString', floatVal=3.14)
        self.assertEqual(self.calledBack, ((42, 'aString'), {'floatVal': 3.14}))
        self.assertEqual(obj.evt1Called, ((42, 'aString'), {'floatVal': 3.14}))
        self.assertEqual(obj.evt2Called, ((42, 'aString'), {'floatVal': 3.14}))
    

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Unittest Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    unittest.main()


