#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import unittest

from TG.common import contextApply

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TestContextApply(unittest.TestCase):
    saved_args = (1,2,3)
    saved_kw = {'a': 1, 'b':2}
    passed_args = (10,20,30)
    passed_kw = {'c': 30, 'b':20}

    def callback(self, *args, **kw):
        return args, kw
    def verify(self, ctxApply, knownGood):
        test = ctxApply(self.callback, *self.saved_args, **self.saved_kw)
        results = test(*self.passed_args, **self.passed_kw)
        self.assertEqual(results, knownGood)

    def testContextApply(self):
        self.verify(contextApply.ContextApply, ((10, 20, 30, 1, 2, 3), {'a': 1, 'c': 30, 'b': 20}))

    def testContextApply_p_s(self):
        self.verify(contextApply.ContextApply_p_s, ((10, 20, 30, 1, 2, 3), {'a': 1, 'c': 30, 'b': 20}))

    def testContextApply_s_p(self):
        self.verify(contextApply.ContextApply_s_p, ((1, 2, 3, 10, 20, 30), {'a': 1, 'c': 30, 'b': 2}))

    def testContextApply_p(self):
        self.verify(contextApply.ContextApply_p, ((10, 20, 30), {'c': 30, 'b': 20}))

    def testContextApply_s(self):
        self.verify(contextApply.ContextApply_s, ((1, 2, 3), {'a': 1, 'b': 2}))

    def testContextApply_0(self):
        self.verify(contextApply.ContextApply_0, ((), {}))
    
class TestBindable(unittest.TestCase):
    saved_args = (1,2,3)
    saved_kw = {'a': 1, 'b':2}
    passed_args = (10,20,30)
    passed_kw = {'c': 30, 'b':20}

    def setUp(self):
        self.bindable = contextApply.Bindable()

    def callback(self, *args, **kw):
        return args, kw
    def verify(self, ctxApply, knownGood):
        test = ctxApply(self.callback, *self.saved_args, **self.saved_kw)
        results = test(*self.passed_args, **self.passed_kw)
        self.assertEqual(results, knownGood)

    def testContextApply(self):
        self.verify(self.bindable.bind, ((10, 20, 30, 1, 2, 3), {'a': 1, 'c': 30, 'b': 20}))

    def testContextApply_p_s(self):
        self.verify(self.bindable.bind_p_s, ((10, 20, 30, 1, 2, 3), {'a': 1, 'c': 30, 'b': 20}))

    def testContextApply_s_p(self):
        self.verify(self.bindable.bind_s_p, ((1, 2, 3, 10, 20, 30), {'a': 1, 'c': 30, 'b': 2}))

    def testContextApply_p(self):
        self.verify(self.bindable.bind_p, ((10, 20, 30), {'c': 30, 'b': 20}))

    def testContextApply_s(self):
        self.verify(self.bindable.bind_s, ((1, 2, 3), {'a': 1, 'b': 2}))

    def testContextApply_0(self):
        self.verify(self.bindable.bind_0, ((), {}))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Unittest Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    unittest.main()


