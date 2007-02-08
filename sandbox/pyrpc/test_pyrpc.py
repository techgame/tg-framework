#!/usr/bin/env python
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

import unittest
import pyrpc

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Thingy(object):
    def _resolveSelector(self, selector):
        if selector.startswith('_'):
            raise Exception("Selector is not allowed to start with an '_'")
        cmd = getattr(self, selector)
        return cmd

    def __call__(self, xml, requestHandler):
        cmd = self._resolveSelector(xml.attrs["selector"])
        return cmd(xml)

    def larry(self, xml): 
        print "larry:", xml
    def shane(self, xml): 
        print "shane:", xml
    def brian(self, xml): 
        print "brian:", xml


class TestServer(unittest.TestCase):
    def setUp(self):
        self.myserver = pyrpc.Server()
        self.myserver.setDispatcher(Thingy())

    def tearDown(self):
        self.myserver.server_close()
        del self.myserver

    def test(self):
        pyrpc.Client().dispatch('larry', "<fluffy white='True'/>", block=False)
        self.myserver.serve_forever()
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Unittest Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    unittest.main()

