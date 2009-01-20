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

import copy
from TG.common.properties import NamedProperty
from TG.notifications.event import Event

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class StateMachineException(Exception): 
    pass
class StateTransitionException(StateMachineException): 
    pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class StateMachinery(object):
    EventFactory = Event

    eachEnterEvent = Event.property()
    eachTransitionEvent = Event.property()
    eachExitEvent = Event.property()

    allowSelfLoops = False
    _initialState = None

    def __init__(self, initialState=NotImplemented, allowSelfLoops=None):
        self.stateEnter = {}
        self.stateExit = {}
        self.transitions = {}

        if initialState is not NotImplemented:
            self.setInitialState(initialState)

        if allowSelfLoops is not None:
            self.allowSelfLoops = allowSelfLoops

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def copy(self):
        return copy.deepcopy(self)

    def getInitialState(self):
        return self._initialState
    def setInitialState(self, initialState):
        self._initialState = initialState
    initialState = property(getInitialState, setInitialState)

    def removeState(self, state):
        """Removes the state from all event tables.
        
        Note: This will not patch the transition paths in state machine.  It
        will simply remove any transition involving the state.
        """
        self.removeStateEnter(state)
        self.removeStateExit(state)
        for fromState, toState in self.iterTransitions(state):
            self.removeTransition(fromState, toState)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def addStateEnterEvent(self, state, sink):
        return self._addEvent(state, sink, self.stateEnter)
    def removeStateEnterEvent(self, state, sink):
        return self._removeEvent(state, sink, self.stateEnter)
    def removeStateEnter(self, state):
        return self._removeKey(state, self.stateEnter)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def addStateExitEvent(self, state, sink):
        return self._addEvent(state, sink, self.stateExit)
    def removeStateExitEvent(self, state, sink):
        return self._removeEvent(state, sink, self.stateExit)
    def removeStateExit(self, state):
        return self._removeKey(state, self.stateExit)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def addTransitionEvent(self, fromState, toState, sink):
        return self._addEvent((fromState, toState), sink, self.transitions)
    def removeTransitionEvent(self, fromState, toState, sink):
        return self._removeEvent((fromState, toState), sink, self.transitions)

    def addTransition(self, fromState, toState):
        return self.addTransitionEvent(fromState, toState, None)
    def removeTransition(self, fromState, toState):
        return self._removeKey((fromState, toState), self.transitions)

    def iterTransitions(self, state):
        for transition in self.transitions.iterkeys():
            if state in transition:
                yield transition

    def iterInbound(self, toState):
        for transition in self.transitions.iterkeys():
            if toState == transition[1]:
                yield iFrom, iTo

    def iterOutbound(self, fromState):
        for transition in self.transitions.iterkeys():
            if fromState == transition[0]:
                yield iFrom, iTo

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _transition(self, obj, fromState, toState):
        if self.allowSelfLoops and fromState == toState:
            return fromState # don't fire events for self-loops
        for event, args in self._iterEvents(fromState, toState):
            event(*args)
        return toState

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _removeKey(self, key, table):
        table.pop(key, None)

    def _addEvent(self, key, sink, table):
        event = table.get(key)
        if event is None:
            event = self.EventFactory()
            table[key] = event

        if sink is None:
            sink = self._emptyHandler

        event.add(sink)
        return sink

    def _emptyHandler(self, *args, **kw):
        pass

    def _removeEvent(self, key, sink, table):
        event = table.get(key)
        if event is None:
            return False
        event.remove(sink)
        return True

    def _iterEvents(self, fromState, toState):
        # Get all the events first. These methods should check for consistency,
        # and will raise in the case of an invalid transition.  
        onExit = self._getStateExitEvent(fromState, toState)
        onTransition = self._getTransitionEvent(fromState, toState)
        onEnter = self._getStateEnterEvent(fromState, toState)

        # Call the events
        yield self.eachExitEvent, ('exit', fromState, toState)
        if onExit is not None: 
            yield onExit, ('exit', fromState, toState)

        yield self.eachTransitionEvent, ('transition', fromState, toState)
        if onTransition is not None: 
            yield onTransition, ('transition', fromState, toState)

        yield self.eachEnterEvent, ('enter', fromState, toState)
        if onEnter is not None: 
            yield onEnter, ('enter', fromState, toState)

    def _getStateEnterEvent(self, fromState, toState):
        return self.stateEnter.get(toState, None)

    def _getStateExitEvent(self, fromState, toState):
        return self.stateExit.get(fromState, None)

    def _getTransitionEvent(self, fromState, toState):
        key = (fromState, toState)
        try:
            event = self.transitions[key]
        except KeyError:
            if fromState is None and toState is self.getInitialState():
                return None
            else:
                raise StateTransitionException('No transition from %r to %r' % key)
        else:
            return event

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class StateMachine(StateMachinery):
    _state = None

    def getState(self):
        return self._state
    def setState(self, toState, doTransition=True):
        if doTransition:
            self.transition(toState)
        else:
            self._state = toState
    state = property(getState, setState)

    def transition(self, toState):
        self._transition(self.getState(), toState)

    def _transition(self, fromState, toState):
        state = StateMachinery._transition(self, fromState, toState)
        self.setState(state, False)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Property
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class StateMachineProperty(StateMachinery, NamedProperty):
    def transition(self, obj, toState):
        self._transition(obj, self.getState(obj), toState)

    def _transition(self, obj, fromState, toState):
        if self.allowSelfLoops and fromState == toState:
            return fromState # don't fire events for self-loops

        for event, args in self._iterEvents(fromState, toState):
            event(obj, *args)

        self.__set__(obj, toState, False)
        return toState

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getState(self, obj):
        return self.__get__(obj)
    def setState(self, obj, toState):
        return self.__set__(obj, toState)

    def __get__(self, obj, klass=None, default=NotImplemented):
        if obj is None:
            return self
        value = self._getObjAttr(obj, '%s_state', default)
        if value is NotImplemented:
            return self._transition(obj, None, self.getInitialState())
        else:
            return value

    def __set__(self, obj, toState, doTransition=True):
        if obj is None:
            return

        if doTransition:
            self.transition(obj, toState)
        else:
            self._setObjAttr(obj, '%s_state', toState)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def onEachEnter(self, method=NotImplemented):
        """Decorator to add the method to fire for each state entry"""
        if method is NotImplemented:
            return self.onEachEnter
        self.eachEnterEvent.add(method)
        return method
    def onStateEnter(self, state):
        """Decorator to add the method to event list for state entry"""
        def _onStateEnter(method):
            self.addStateEnterEvent(state, method)
            return method
        return _onStateEnter
    onEnter = onEntry = onStateEntry = onStateEnter

    def onEachExit(self, method=NotImplemented):
        """Decorator to add the method to fire for each state exit"""
        if method is NotImplemented:
            return self.onEachExit
        self.eachExitEvent.add(method)
        return method
    def onStateExit(self, state):
        """Decorator to add the method to event list for state exit"""
        def _onStateExit(method):
            self.addStateExitEvent(state, method)
            return method
        return _onStateExit
    onExit = onStateExit

    def onEachTransition(self, method=NotImplemented):
        """Decorator to add the method to fire for each state transition"""
        if method is NotImplemented:
            return self.onEachTransition
        self.eachTransitionEvent.add(method)
        return method
    def onTransition(self, fromState, toState):
        """Decorator to add the method to event list for transition entry"""
        def _onTransition(method):
            self.addTransitionEvent(fromState, toState, method)
            return method
        return _onTransition
    onTrans = onTransition

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    class Example(object):
        state = StateMachineProperty('A')

        def __init__(self):
            assert self.state == 'A'
            self.state = 'B'
            Example.state.transition(self, 'C')
            self.state = 'Done'

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        @state.onEachEnter()
        def onEachEnter(self, changeType, fromState, toState):
            print
            print 'onEachEnter: %r from: %r to: %r' % (changeType, fromState, toState)
        @state.onEachExit()
        def onEachExit(self, changeType, fromState, toState):
            print
            print 'onEachExit: %r from: %r to: %r' % (changeType, fromState, toState)
        @state.onEachTransition()
        def onEachTransition(self, changeType, fromState, toState):
            print
            print 'onEachTransition: %r from: %r to: %r' % (changeType, fromState, toState)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        @state.onEnter('A')
        def onEnterA(self, changeType, fromState, toState):
            print 'onEnterA: %r from: %r to: %r' % (changeType, fromState, toState)

        @state.onExit('A')
        def onExitA(self, changeType, fromState, toState):
            print 'onExitA: %r from: %r to: %r' % (changeType, fromState, toState)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        @state.onTrans('A', 'B')
        def onTransAtoB(self, changeType, fromState, toState):
            print 'onTransAtoB: %r from: %r to: %r' % (changeType, fromState, toState)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        @state.onEnter('B')
        def onEnterB(self, changeType, fromState, toState):
            print 'onEnterB: %r from: %r to: %r' % (changeType, fromState, toState)

        @state.onExit('B')
        def onExitB(self, changeType, fromState, toState):
            print 'onExitB: %r from: %r to: %r' % (changeType, fromState, toState)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        @state.onTrans('B', 'C')
        def onTransBtoC(self, changeType, fromState, toState):
            print 'onTransBtoC: %r from: %r to: %r' % (changeType, fromState, toState)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        @state.onEnter('C')
        def onEnterC(self, changeType, fromState, toState):
            print 'onEnterC: %r from: %r to: %r' % (changeType, fromState, toState)

        @state.onExit('C')
        def onExitC(self, changeType, fromState, toState):
            print 'onExitC: %r from: %r to: %r' % (changeType, fromState, toState)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        @state.onTrans('C', 'Done')
        def onTransCtoDone(self, changeType, fromState, toState):
            print 'onTransCtoDone: %r from: %r to: %r' % (changeType, fromState, toState)

        @state.onEnter('Done')
        def onDone(self, changeType, fromState, toState):
            print 'onDone: %r from: %r to: %r' % (changeType, fromState, toState)

    t = Example()

