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

import time
from TG.common.bindCallable import weakBind

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TaskBase(object):
    def isTaskReady(self, incIdle=True):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

    def runTask(self):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

    def runTaskWithTimeout(self, timeout):
        time.sleep(timeout)

    def runFromTaskList(self, taskList):
        return self.runTask()

    def runTaskLoop(self, *args, **kw):
        while self.isTaskReady():
            self.runTask(*args, **kw)

    def onAddToTaskList(self, taskList):
        pass
    def onRemoveFromTaskList(self, taskList):
        pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class DelegateTask(TaskBase):
    def __init__(self, methodRun, methodIsReady=lambda: True):
        self.methodRun = weakBind(methodRun)
        self.methodIsReady = weakBind(methodIsReady)

    def isTaskReady(self, incIdle=True):
        isReady = self.methodIsReady
        if isReady:
            return isReady()
    def runTask(self):
        run = self.methodRun
        if run:
            return run()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Task(TaskBase):
    _enabled = True

    def isTaskReady(self, incIdle=True):
        return bool(self.isEnabled())

    def isEnabled(self):
        return self._enabled
    def enable(self, enabled=True):
        self._enabled = enabled

    def isDisabled(self):
        return not self.isEnabled()
    def disable(self):
        self.enable(False)

    def runFromTaskList(self, taskList):
        try:
            result = self.runTask()
        except StopIteration:
            self.disable()

        self._updateTaskOnList(taskList)
        return result

    def _updateTaskOnList(self, taskList):
        if self.isDisabled():
            taskList.removeTask(self)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Specific Subcases
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CallableTask(Task):
    def __init__(self, callback, *args, **kw):
        Task.__init__(self)
        self._callArgsKw = (callback, args, kw)

    def __ne__(self, other):
        return not self == other
    def __eq__(self, other):
        if self is other:
            return True
        elif not isinstance(other, TaskBase):
            return (self._callArgsKw == other) or (self._callArgsKw[0] == other)
        return False

    _single = False
    def getSingle(self):
        return self._single
    def setSingle(self, single=True):
        self._single = single
    single = property(getSingle, setSingle)

    def runTask(self):
        callback, args, kw = self._callArgsKw
        callback(*args, **kw)
        if self.getSingle():
            self.disable()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class IterableTask(Task):
    iter = None
    _callArgsKw = None

    def __init__(self, iter):
        Task.__init__(self)
        self.iter = iter

    def __ne__(self, other):
        return not self == other
    def __eq__(self, other):
        if self is other:
            return True
        elif not isinstance(other, TaskBase):
            return (self._callArgsKw == other) or (self._callArgsKw[0] == other)
        return False

    def runTask(self):
        try:
            self.iter.next()
            return True
        except StopIteration:
            self.disable()
            return False

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SimpleTask(IterableTask):
    def __init__(self, iterOrCallback=None, *args, **kw):
        if callable(iterOrCallback):
            self._callArgsKw = (iterOrCallback, args, kw)
            iter = self._iterBootstrap()
        else:
            iter = iterOrCallback

        IterableTask.__init__(self, iter)

    def _iterBootstrap(self):
        callback, args, kw = self._callArgsKw
        iter = callback(*args, **kw)
        if iter is not None:
            # replace our iterator, and return the next value
            self.iter = iter 
            yield self.iter.next()
        else:
            self.iter = self._iterCalls()
            yield None

    def _iterCalls(self):
        callback, args, kw = self._callArgsKw
        while 1:
            yield callback(*args, **kw)

