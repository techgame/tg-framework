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

import socket
from SocketServer import TCPServer, BaseRequestHandler

import md5

from TG.w3c import xmlNode

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ChatterException(Exception): pass
class ChatterNAK(ChatterException): pass
class ChatterNoResponse(ChatterException): pass

class Chatter(object):
    _chunkSize = 1024

    def _hashOf(self, data):
        return 'md5:' + md5.md5(data).hexdigest()

    def _getSocket(self):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

    def _rawRecv(self):
        data = ""
        sock = self._getSocket()
        sock.settimeout(0.1)
        try:
            while sock:
                part = sock.recv(self._chunkSize)
                data += part
                if len(part) < self._chunkSize:
                    break # no more data in chunk
        except socket.error:
            return None
        except socket.timeout:
            return None
        return data

    def _rawSend(self, data):
        self._getSocket().sendall(data)

    def xmlRecv(self, sendAck=False):
        data = self._rawRecv()
        if data is None:
            return None
        
        xmlProducer = xmlNode.Producer()
        xml = ''.join(["<pyrpc-frame>", data, "</pyrpc-frame>"])

        #0/0
        try:
            xml = xmlProducer.parse(xml)
        except Exception, e:
            if sendAck:
                nak = xmlNode.XMLNode('nak')
                nak.attrs['hash'] = self._hashOf(data)
                nak.attrs['reason'] = str(e)
                self.xmlSend(nak, False)
            self._getSocket().shutdown(2)
            raise
        else: 
            if sendAck:
                nak = xmlNode.XMLNode('ack')
                nak.attrs['hash'] = self._hashOf(data)
                self.xmlSend(nak, False)

        return xml.listNodes()

    def xmlRecvIter(self, sendAck=False):
        while 1:
            r = self.xmlRecv(sendAck)
            if r is None:
                return
            yield r

    def xmlSend(self, xml, checkAck=False):
        data = str(xml)
        self._rawSend(data)

        if checkAck:
            xml = self.xmlRecv(False)
            if not xml:
                raise ChatterNoResponse("No response")

            xml = xml[0]
            if xml.attrs['hash'] != self._hashOf(data):
                raise ChatterError("Data hash mismatch")
            elif xml.node == 'nak':
                raise ChatterNAK("NAK")
            elif xml.node == 'ack':
                return True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class RequestHandler(BaseRequestHandler, Chatter):
    """
    request -- the socket we accepted for this request
    client_address -- the address of whoever called us
    server -- an instance of Server (below)
    """

    def _getSocket(self):
        return self.request

    def setup(self):
        pass

    def handle(self):
        for xmlList in self.xmlRecvIter(True):
            for xml in xmlList:
                cmd = self.dispatch.get(xml.node, self.cmd_error)
                cmd(self, xml)

    def finish(self):
        pass

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    dispatch = {}
    def cmd_stopServer(self, xml):
        self.server.serve_forever(False)
    dispatch['stopServer'] = cmd_stopServer

    def cmd_dispatch(self, xml):
        dispatcher = self.server.getDispatcher()
        return dispatcher(xml, self)
    dispatch['dispatch'] = cmd_dispatch

    def cmd_error(self, xml):
        pass
    dispatch['error'] = cmd_error


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Server(TCPServer):
    _dispatcher = None

    def __init__(self, server_address=('0.0.0.0', 10005), RequestHandlerClass=RequestHandler):
        TCPServer.__init__(self, server_address, RequestHandlerClass)

    def serve_forever(self, bServing=True):
        self._stillServing = bServing
        while self._stillServing:
            self.handle_request()

    def handle_request(self):
        if self.getDispatcher() is None:
            raise Exception("Call setDispatcher() before handling requests")
        return TCPServer.handle_request(self)

    def getDispatcher(self):
        return self._dispatcher
    def setDispatcher(self, dispatcher):
        self._dispatcher = dispatcher

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Client(Chatter):
    sock = None

    def __init__(self, address=None):
        if address is not None:
            self.connect(address)

    def __del__(self):
        self.disconnect()

    def _getSocket(self):
        if not self.sock:
            self.connect()
        return self.sock

    def connect(self, address=('localhost', 10005)):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(address)

    def shutdown(self):
        self.sock.shutdown(2)
    def disconnect(self):
        if self.sock:
            self.sock.close()
            del self.sock

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def dispatch(self, selector, *args, **kw):
        xml = xmlNode.XMLNode('dispatch')
        xml.attrs['selector'] = selector
        map(xml.addExplicit, args)
        return self.xmlSend(xml, kw.pop('block', True))

    def stopServer(self, selector, *args, **kw):
        return self.xmlSend('<stopServer/>', kw.pop('block', True))

