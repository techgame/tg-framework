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

import sets
from TG.common import properties

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class GraphNode(object):
    inbound = properties.LazyProperty(list)
    outbound = properties.LazyProperty(list)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def iterOutbound(self):
        return iter(self.outbound)
    def iterInbound(self):
        return iter(self.inbound)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def linkTo(self, otherNode, recurse=True):
        self.outbound.append(otherNode)
        if recurse:
            otherNode.linkFrom(self, False)

    def unlinkTo(self, otherNode, recurse=True):
        if otherNode in self.outbound:
            self.outbound.remove(otherNode)
        if recurse:
            otherNode.unlinkFrom(self, False)

    def unlinkToAll(self, otherNode, recurse=True):
        for each in self.iterOutbound():
            self.unlinkFrom(each, recurse)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def linkFrom(self, otherNode, recurse=True):
        self.inbound.append(otherNode)
        if recurse:
            otherNode.linkTo(self, False)

    def unlinkFrom(self, otherNode, recurse=True):
        if otherNode in self.inbound:
            self.inbound.remove(otherNode)
        if recurse:
            otherNode.unlinkTo(self, False)

    def unlinkFromAll(self, otherNode, recurse=True):
        for each in self.iterInbound():
            self.unlinkFrom(each, recurse)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def unlinkAll(self, recurse=True):
        self.unlinkFromAll(recurse)
        self.unlinkToAll(recurse)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Search Algorithms
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class GraphSearch(object):
    def search(self, root, visitCB, *args, **kw):
        visitedSet = self.createVisitSet()
        for item in self.iterVisitItems(root, visitedSet):
            result = visitCB(item, *args, **kw)
        return result
    __call__ = search

    def iterVisitItems(self, node, visitedSet=None):
        if self.visitNode(node, visitedSet):
            raise NotImplementedError('Subclass Responsibility: %r' % (self,))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def createVisitSet(self):
        return sets.Set()

    def visitNode(self, node, visitedSet):
        if node not in visitedSet:
            visitedSet.add(node)
            return True
        else:
            return False

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class InboundGraphSearch(GraphSearch):
    def iterVisitItems(self, node, visitedSet):
        if self.visitNode(node, visitedSet):
            yield node
            for each in node.iterInbound():
                for eachResult in self.iterVisitItems(each, visitedSet):
                    yield eachResult


class OutboundGraphSearch(GraphSearch):
    def iterVisitItems(self, node, visitedSet):
        if self.visitNode(node, visitedSet):
            yield node
            for each in node.iterOutbound():
                for eachResult in self.iterVisitItems(each, visitedSet):
                    yield eachResult

class InOrderGraphSearch(GraphSearch):
    def iterVisitItems(self, node, visitedSet):
        if self.visitNode(node, visitedSet):
            for each in node.iterInbound():
                for eachResult in self.iterVisitItems(each, visitedSet):
                    yield eachResult
            yield node
            for each in node.iterOutbound():
                for eachResult in self.iterVisitItems(each, visitedSet):
                    yield eachResult

