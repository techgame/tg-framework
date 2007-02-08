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

class NonblockingChannel(stackless.channel):
    def send(self, value, wait=False):
        if wait or self.balance < 0: 
            # there are tasklets waiting to receive
            return stackless.channel.send(self, value)
    def send_exception(self, exc, value, wait=False):
        if wait or self.balance < 0: 
            # there are tasklets waiting to receive
            return stackless.channel.send_exception(self, exc, value)
    def receive(self, default=None, wait=False):
        if wait or self.balance > 0:
            # there are tasklets waiting to send
            return stackless.channel.receive(self)
        else:
            return default

def testNonblockingChannel():
    print
    print "testNonblockingChannel"
    print "----------------------"

    def recv(ch, name):
        print "Started recv<%s>" % (name,)
        print 'recv<%s>: got a message from "%s"' % (name, ch.receive(wait=True))
        ch.send(name)

    ch = NonblockingChannel()
    ch.receive() # nonblocking receive
    ch.send("nonblocking!") # nonblocking send

    for name in "ABCDE":
        task = stackless.tasklet(recv)(ch, name)
        task.run()

    ch.send('host')
    print

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class BroadcastChannel(stackless.channel):
    def send(self, value, wait=False):
        result = None
        for idx in range(0, self.balance, -1):
            # there are tasklets waiting to receive
            result = stackless.channel.send(self, value)
        return result
    def send_exception(self, exc, value, wait=False):
        result = None
        for idx in range(0, self.balance, -1):
            # there are tasklets waiting to receive
            result = stackless.channel.send_exception(self, exc, value)
        return result

def testBroadcastChannel():
    print
    print "testBroadcastChannel"
    print "--------------------"
    def recv(ch, name):
        print "Started recv<%s>" % (name,)
        print "recv<%s>: %r" % (name, ch.receive())

    ch = BroadcastChannel()

    # Essentially nonblocking on sends when there are no receivers
    ch.send("Test when empty")

    for name in "ABCDE":
        task = stackless.tasklet(recv)(ch, name)
        task.run()

    ch.send("broadcast from host")
    print
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    testNonblockingChannel()
    testBroadcastChannel()
