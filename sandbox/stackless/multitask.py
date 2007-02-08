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
import pickle

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def runMultitaskInner(instructions=1000):
    lastTasklet = stackless.run(instructions)
    if lastTasklet is not None:
        # put it back in the scheduler
        lastTasklet.insert() 
        return True
    return False

def runMultitask(instructions=1000):
    print "running multitask:"
    while runMultitaskInner(instructions):
        pass
    print "exiting multitask:"


def testMultitask():
    print 
    print "testMultitask"
    print "-------------"
    def aCallable(name, count=10000, mod=1000):
        for each in xrange(count):
            if each % mod == 0:
                print "aCallable<%s>: %r" % (name, each)

    for name in "ABCDE":
        stackless.tasklet(aCallable)(name).insert()

    runMultitaskInner()
    import threading
    t = threading.Thread(None, runMultitask)
    t.start()
    t.join()
    print
    runMultitask()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    testMultitask()

