#!/usr/bin/env python
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

import unittest
from pprint import pprint

from TG.notifications.stateMachine import StateMachineProperty, StateTransitionException

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TestStateMachineProperty(unittest.TestCase):
    state = StateMachineProperty('A')

    def setUp(self):
        self.data = []
    def tearDown(self):
        del self.data

    def clearData(self):
        del self.data[:]
    def checkData(self, shouldBe):
        if self.data != shouldBe:
            print
            pprint(self.data)
        self.assertEqual(self.data, shouldBe)
        self.clearData()

    def testEmpty(self):
        self.checkData([])

    def testA(self):
        assert self.state == 'A'
        self.checkData(
            ['each exit None A',
            'each transition None A',
            'each enter None A',
            'enter None A'])

    def testB(self):
        assert self.state == 'A'
        self.clearData()

        self.state = 'B'
        self.checkData(
            ['each exit A B',
            'exit A B',
            'each transition A B',
            'transition A B',
            'each enter A B',
            'enter A B'])

    def testC(self):
        assert self.state == 'A'
        self.state = 'B'
        self.clearData()

        type(self).state.transition(self, 'C')
        self.checkData(
            ['each exit B C',
            'exit B C',
            'each transition B C',
            'transition B C',
            'each enter B C',
            'enter B C'])

    def testDone(self):
        assert self.state == 'A'
        self.state = 'B'
        self.state = 'C'
        try:
            self.state = 'Done'
        except StateTransitionException:
            pass
        else:
            self.fail("Invalid transition did not raise proper exception")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @state.onEachExit()
    def onEachExit(self, changeType, fromState, toState):
        self.assertEqual(changeType, 'exit')
        self.data.append('each %s %s %s' % (changeType, fromState, toState))
    @state.onEachTransition()
    def onEachTransition(self, changeType, fromState, toState):
        self.assertEqual(changeType, 'transition')
        self.data.append('each %s %s %s' % (changeType, fromState, toState))
    @state.onEachEnter()
    def onEachEnter(self, changeType, fromState, toState):
        self.assertEqual(changeType, 'enter')
        self.data.append('each %s %s %s' % (changeType, fromState, toState))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @state.onEnter('A')
    def onEnterA(self, changeType, fromState, toState):
        self.assertEqual(changeType, 'enter')
        self.assertEqual(fromState, None)
        self.assertEqual(toState, 'A')
        self.data.append('%s %s %s' % (changeType, fromState, toState))
    @state.onExit('A')
    def onExitA(self, changeType, fromState, toState):
        self.assertEqual(changeType, 'exit')
        self.assertEqual(fromState, 'A')
        self.assertEqual(toState, 'B')
        self.data.append('%s %s %s' % (changeType, fromState, toState))
    @state.onTrans('A', 'B')
    def onTransAtoB(self, changeType, fromState, toState):
        self.assertEqual(changeType, 'transition')
        self.assertEqual(fromState, 'A')
        self.assertEqual(toState, 'B')
        self.data.append('%s %s %s' % (changeType, fromState, toState))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @state.onEnter('B')
    def onEnterB(self, changeType, fromState, toState):
        self.assertEqual(changeType, 'enter')
        self.assertEqual(fromState, 'A')
        self.assertEqual(toState, 'B')
        self.data.append('%s %s %s' % (changeType, fromState, toState))
    @state.onExit('B')
    def onExitB(self, changeType, fromState, toState):
        self.assertEqual(changeType, 'exit')
        self.assertEqual(fromState, 'B')
        self.assertEqual(toState, 'C')
        self.data.append('%s %s %s' % (changeType, fromState, toState))
    @state.onTrans('B', 'C')
    def onTransBtoC(self, changeType, fromState, toState):
        self.assertEqual(changeType, 'transition')
        self.assertEqual(fromState, 'B')
        self.assertEqual(toState, 'C')
        self.data.append('%s %s %s' % (changeType, fromState, toState))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @state.onEnter('C')
    def onEnterC(self, changeType, fromState, toState):
        self.assertEqual(changeType, 'enter')
        self.assertEqual(fromState, 'B')
        self.assertEqual(toState, 'C')
        self.data.append('%s %s %s' % (changeType, fromState, toState))
    @state.onExit('C')
    def onExitC(self, changeType, fromState, toState):
        self.assertEqual(changeType, 'exit')
        self.assertEqual(fromState, 'C')
        self.assertEqual(toState, 'Done')
        self.data.append('%s %s %s' % (changeType, fromState, toState))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TestDerivedStateMachineProperty(TestStateMachineProperty):
    state = TestStateMachineProperty.state.copy()

    def testDone(self):
        assert self.state == 'A'
        self.state = 'B'
        self.state = 'C'
        self.clearData()

        self.state = 'Done'
        self.checkData(
            ['each exit C Done',
            'exit C Done',
            'each transition C Done',
            'transition C Done',
            'each enter C Done',
            'enter C Done'])

    @state.onTrans('C', 'Done')
    def onTransCtoDone(self, changeType, fromState, toState):
        self.assertEqual(changeType, 'transition')
        self.assertEqual(fromState, 'C')
        self.assertEqual(toState, 'Done')
        self.data.append('%s %s %s' % (changeType, fromState, toState))

    @state.onEnter('Done')
    def onDone(self, changeType, fromState, toState):
        self.assertEqual(changeType, 'enter')
        self.assertEqual(fromState, 'C')
        self.assertEqual(toState, 'Done')
        self.data.append('%s %s %s' % (changeType, fromState, toState))

    @state.onExit('Done')
    def onDone(self, changeType, fromState, toState):
        self.fail("Should never exit the Done state")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Unittest Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    unittest.main()

