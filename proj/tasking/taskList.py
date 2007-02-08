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

from TG.tasking.task import TaskBase, DelegateTask, SimpleTask, CallableTask, IterableTask
from TG.tasking.properties import TaskListPropertyFactory

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Task List
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TaskListBase(TaskBase, TaskListPropertyFactory):
    def __iter__(self):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def isTaskReady(self, incIdle=True):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    _idle = None
    def getIdleTask(self):
        return self._idle
    def setIdleTask(self, idleTaskItem, andAddTask=False):
        self._idle = idleTaskItem
        if andAddTask:
            self.addTask(idleTaskItem)
        return idleTaskItem
    def delIdleTask(self, andRemoveTask=False):
        idle = self._idle
        if idle is not None:
            del self._idle
            self.removeTask(idle)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def addTask(self, taskItem):
        if self._addTaskToList(taskItem):
            taskItem.onAddToTaskList(self)
            return taskItem
        else:
            return None

    def removeTask(self, taskItem):
        if taskItem is not None:
            if taskItem is self.getIdleTask():
                self.delIdleTask()
            taskItem = self._removeTaskFromList(taskItem)
            if taskItem is not None:
                taskItem.onRemoveFromTaskList(self)
                return taskItem
        else:
            return None

    def hasTask(self, taskItem):
        return self._hasTaskInList(taskItem)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _addTaskToList(self, taskItem):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def _removeTaskFromList(self, taskItem):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def _hasTaskInList(self, taskItem):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def _selectTask(self):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def runTask(self, timeout=0):
        taskItem = self._selectTask()
        if taskItem is not None:
            self._runTaskItemFromSelf(taskItem)
            return True
        elif timeout:
            idleTask = self.getIdleTask()
            if idleTask is not None:
                idleTask.runTaskWithTimeout(timeout)
                return True
        return False
    run = runTask

    def runTaskWithTimeout(self, timeout):
        return self.runTask(timeout)

    def _runTaskItemFromSelf(self, taskItem):
        return taskItem.runFromTaskList(self)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TaskListExtendedBase(TaskListBase):
    DelegateTaskFactory = DelegateTask
    SimpleTaskFactory = SimpleTask
    CallableTaskFactory = CallableTask
    IterableTaskFactory = IterableTask

    def __contains__(self, value):
        if isinstance(value, tuple):
            value = (value[0], value[1:], {})
            self.hasTask(value)
        else:
            self.hasTask(value)

    def __iadd__(self, value):
        if isinstance(value, tuple):
            self.add(*value)
        else:
            self.add(value)
        return self

    def __isub__(self, value):
        if isinstance(value, tuple):
            value = (value[0], value[1:], {})
            self.removeTask(value)
        else:
            self.removeTask(value)
        return self

    def setIdleTask(self, idleTaskItem, andAddTask=False):
        idleTaskItem = self._itemAsTask(idleTaskItem)
        return TaskListBase.setIdleTask(self, idleTaskItem, andAddTask)

    def add(self, arg0, *args, **kw):
        taskItem = self._itemAsTask(arg0, *args, **kw)
        return self.addTask(taskItem)

    def addDelegate(self, methodRun, methodIsReady=lambda: True):
        taskItem = self.DelegateTaskFactory(methodRun, methodIsReady)
        return self.addTask(taskItem)

    def addCallMany(self, *args, **kw):
        taskItem = self.CallableTaskFactory(*args, **kw)
        taskItem.setSingle(False)
        return self.addTask(taskItem)

    def addCallOnce(self, *args, **kw):
        taskItem = self.CallableTaskFactory(*args, **kw)
        taskItem.setSingle(True)
        return self.addTask(taskItem)

    def addIter(self, *args, **kw):
        taskItem = self.IterableTaskFactory(*args, **kw)
        return self.addTask(taskItem)

    def _itemAsTask(self, arg0, *args, **kw):
        if isinstance(arg0, TaskBase):
            return arg0
        return self.SimpleTaskFactory(arg0, *args, **kw)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Round Robbin Task List
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class RoundRobbinTaskList(TaskListExtendedBase):
    _tasks = None # list
    _idx = 0

    def __iter__(self):
        return iter(self.getTasks())

    def getTasks(self):
        if self._tasks is None:
            self._tasks = []
        return self._tasks

    def isTaskReady(self, incIdle=True):
        if incIdle:
            idleTask = self.getIdleTask()
            if idleTask is not None:
                return True
        for t in self.getTasks():
            if t.isTaskReady(False):
                return True
        return False

    def _currentTask(self):
        tasks = self.getTasks()
        if tasks:
            return tasks[self._idx]
        else: return None

    def _selectTask(self):
        startIdx = self._idx
        while 1:
            taskItem = self._currentTask()
            if taskItem is None:
                return None

            self._incIdx(+1)
            if taskItem.isTaskReady(False):
                return taskItem
            elif self._idx == startIdx:
                return None

    def _incIdx(self, delta=1):
        taskCount = len(self.getTasks())
        if taskCount:
            self._idx = (self._idx + delta) % taskCount
        else:
            self._idx = 0
        return self._idx

    def _hasTaskInList(self, taskItem):
        return taskItem in self.getTasks()

    def _addTaskToList(self, taskItem):
        if taskItem is not None:
            self.getTasks().append(taskItem)
            return True
        else:
            return False

    def _removeTaskFromList(self, taskItem):
        tasks = self.getTasks()
        try: 
            idx = tasks.index(taskItem)
        except ValueError:
            return None

        taskItem = tasks.pop(idx)
        self._incIdx((idx < self._idx) and -1 or 0)
        return taskItem

