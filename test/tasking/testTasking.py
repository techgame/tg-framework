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
from TG.tasking.taskList import RoundRobbinTaskList

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TestTasking(unittest.TestCase):
    def setUp(self):
        self.log = []
        self.taskList = RoundRobbinTaskList()

    def tearDown(self):
        del self.log
        del self.taskList

    def logger(self, fmt, count):
        for i in xrange(count):
            self.log.append(fmt % (i,))
            yield None

    def loggerCall(self, fmt, count):
        for i in xrange(count):
            self.log.append(fmt % (i,))


    def testOneSimpleTask(self):
        self.taskList.add(self.logger, 'A: %d', 3)
        self.taskList.runTaskLoop()
        self.assertEqual(self.log, ['A: 0', 'A: 1', 'A: 2'])

    def testOneSimpleTask2(self):
        self.taskList.add(self.logger('B: %d', 3))
        self.taskList.runTaskLoop()
        self.assertEqual(self.log, ['B: 0', 'B: 1', 'B: 2'])

    def testOneIterTask(self):
        self.taskList.addIter(self.logger('C: %d', 4))
        self.taskList.runTaskLoop()
        self.assertEqual(self.log, ['C: 0', 'C: 1', 'C: 2', 'C: 3'])

    def testOneCallTask(self):
        self.taskList.addCallOnce(self.loggerCall, 'Call: %d', 2)
        self.taskList.runTaskLoop()
        self.assertEqual(self.log, ['Call: 0', 'Call: 1'])

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testThreeSimpleTasks(self):
        self.taskList.add(self.logger, 'A: %d', 3)
        self.taskList.add(self.logger, 'B: %d', 5)
        self.taskList.add(self.logger, 'C: %d', 7)
        self.taskList.runTaskLoop()
        self.assertEqual(self.log, [
            'A: 0', 'B: 0', 'C: 0',
            'A: 1', 'B: 1', 'C: 1',
            'A: 2', 'B: 2', 'C: 2',
                    'B: 3', 'C: 3',
                    'B: 4', 'C: 4',
                            'C: 5',
                            'C: 6', ])

    def testThreeSimpleTasksIAdd(self):
        self.taskList += (self.logger, 'A: %d', 3)
        self.taskList += (self.logger, 'B: %d', 5)
        self.taskList += (self.logger, 'C: %d', 7)
        self.taskList.runTaskLoop()
        self.assertEqual(self.log, [
            'A: 0', 'B: 0', 'C: 0',
            'A: 1', 'B: 1', 'C: 1',
            'A: 2', 'B: 2', 'C: 2',
                    'B: 3', 'C: 3',
                    'B: 4', 'C: 4',
                            'C: 5',
                            'C: 6', ])

    def testThreeSimpleTasksIAddIRemove(self):
        self.taskList += (self.logger, 'A: %d', 3)
        self.taskList += (self.logger, 'B: %d', 5)
        self.taskList += (self.logger, 'C: %d', 7)

        for x in xrange(6): 
            self.taskList.run()

        self.assertEqual(self.log, [
            'A: 0', 'B: 0', 'C: 0',
            'A: 1', 'B: 1', 'C: 1', ])

        self.taskList -= (self.logger, 'B: %d', 5)

        for x in xrange(5): 
            self.taskList.run()

        self.assertEqual(self.log, [
            'A: 0', 'B: 0', 'C: 0',
            'A: 1', 'B: 1', 'C: 1',
            'A: 2',         'C: 2',
                            'C: 3',
                            'C: 4', ])

        self.taskList -= self.logger

        self.taskList.runTaskLoop()

        self.assertEqual(self.log, [
            'A: 0', 'B: 0', 'C: 0',
            'A: 1', 'B: 1', 'C: 1',
            'A: 2',         'C: 2',
                            'C: 3',
                            'C: 4', ])

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Unittest Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    unittest.main()

