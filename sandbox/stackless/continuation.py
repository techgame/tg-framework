##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##~ Copyright (C) 2002-2004  TechGame Networks, LLC.
##~ 
##~ This library is free software; you can redistribute it and/or
##~ modify it under the terms of the BSD style License as found in the 
##~ LICENSE file included with this distribution.
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import stackless
import time
import copy

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

branchingChannel = stackless.channel()
def branch(tasklet=None):
    if tasklet is None:
        tasklet = stackless.getcurrent()
        capture = stackless.tasklet().capture()
    branchingChannel.send(tasklet)
    tasklet.insert()
    return True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TaskletContinationTest(object):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    copiedBranches = None
    branchingChannel = branchingChannel

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Definitions 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __init__(self):
        self.createBrancherTasklet()

    def test(self):
        start = time.time()
        print "Begin runing origonal tasks"
        count = stackless.getruncount()
        self.runTasklets()
        print "End runing origonal tasks"

        print "Begin restoring copied tasks"
        while self.getCopiedBranches():
            tasklet = self.getCopiedBranches().pop(0)
            print "  Restoring copied task"
            count += 1
            tasklet.insert()

            self.runTasklets()
        print "End restoring copied tasks"

        delta = time.time()-start
        print
        print "Ran %d branched tasklets in: %.2fs" % (count, delta, )
        print "    average tasklet process time: %.2e" % (delta/count,)
        print

    def runTasklets(self):
        stackless.run()

    def saveTasklet(self, tasklet):
        self.getCopiedBranches().append(copy.deepcopy(tasklet))

    def getCopiedBranches(self):
        if self.copiedBranches is None:
            self.copiedBranches = []
        return self.copiedBranches

    def __getstate__(self):
        assert False, "I don't want to be pickled"

    def brancherTask(self):
        while True:
            tasklet = self.branchingChannel.receive()
            self.saveTasklet(tasklet)
    def createBrancherTasklet(self):
        return stackless.tasklet(self.brancherTask)().insert()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Test Definitions
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MyTestTaskObj(object):
    def __init__(self, name, count):
        self.name = name
        self.count = count
    def __repr__(self):
        return "%s<%x>" % (self.name, id(self))

    def doStuff(self):
        start = time.time()
        print "  Starting %r" % (self,)
        for i in range(self.count):
            print "    %r: %d" % (self, i)
            branch()
        delta = time.time()-start
        print "  Ending %r: %.2fs" % (self, delta)
        print

    def createTassklet(klass, *args, **kw):
        return stackless.tasklet(klass(*args, **kw).doStuff)().insert()
    createTassklet = classmethod(createTassklet)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    tester = TaskletContinationTest()
    for name in "A":
        MyTestTaskObj.createTassklet(name, count=4)
    #for name in "ABCD":
    #    MyTestTaskObj.createTassklet(name, count=4)
    tester.test()

