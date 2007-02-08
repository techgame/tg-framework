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

def testPickle():
    print 
    print "testPickle"
    print "----------"
    def aCallable(name):
        print "  aCallable<%s>: Before schedule()" % (name,)
        stackless.schedule()
        print "  aCallable<%s>: After schedule()" % (name,)

    tasks = [stackless.tasklet(aCallable)(name) for name in "ABCDE"]

    print "schedule():"
    stackless.schedule()
    print

    print "pickling..."
    outfile = file('tasks.pickle', 'wb')
    pickle.dump(tasks, outfile, 2)
    outfile.close()
    print

    print "run():"
    stackless.run()
    print

    print

def testUnpickle():
    print
    print "testUnpickle"
    print "------------"

    infile = file('tasks.pickle', 'rb')
    tasks = pickle.load(infile)
    infile.close()

    print "tasks:", [t.alive for t in tasks]
    for task in tasks:
        task.insert()
    print "run() unpickled tasks:"
    stackless.run()
    print


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    #testPickle()
    testUnpickle()

