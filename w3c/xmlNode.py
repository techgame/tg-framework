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

from types import SliceType as _SliceType
from xml.sax.saxutils import quoteattr as xmlquoteattr
from xml.sax.saxutils import escape as xmlescape

from xmlNamespaceMap import XMLNamespaceMap

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

linesep = '\n'

_NodeKeyOrSlice = (int, long, _SliceType)

class Any(object):
    def __eq__(self, other): return True
    def __ne__(self, other): return False
Any = Any()

class MatchObj(object):
    def __init__(self, testcall):
        self.testcall = testcall
    def __eq__(self, other):
        return bool(self.testcall(other))

truelambda = lambda each: True
falselambda = lambda each: False

def makeNodeMatcher(*args, **kw):
    if args or kw:
        return makeNodeMatcherEx(*args, **kw)
    else: return truelambda

def makeNodeMatcherEx(node=Any, namespace=Any, prefix=Any, **kw):
    if 'xmlns' in kw:
        namespace = kw.pop('xmlns')
    def nodematcher(each):
        if isinstance(each, basestring): return node==each
        else: return node==each.node and namespace==each.namespace and prefix==each.prefix
    return nodematcher

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class XMLNodeBase(object): 
    node = None
    namespace = None
    prefix = None

    def __str__(self):
        """Returns XMLNode as a string in XML form."""
        return str(self.toXML())

    def asXMLNode(self):
        return self

    def toXML(self, pretty=False, level=0, indent='    ', newline=linesep):
        raise NotImplementedError

    def encode(self, *args, **kw):
        return self.toXML().encode(*args, **kw)

    def decode(self, *args, **kw):
        return self.toXML().decode(*args, **kw)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class XMLExplicit(XMLNodeBase):
    explicit = ''

    def __init__(self, explicit=''):
        self.setExplicit(explicit)

    def toXML(self, pretty=False, level=0, indent='    ', newline=linesep):
        result = self.getExplicit()
        if not pretty:
            return result
        else:
            return result.replace(newline, newline+indent*level)

    def __cmp__(self, other):
        return cmp(self.getExplicit(), other)

    def getExplicit(self):
        return self.explicit
    def setExplicit(self, explicit):
        self.explicit = explicit

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class XMLComment(XMLNodeBase):
    comment = ''
    def __init__(self, comment=''):
        self.setComment(comment)

    def toXML(self, pretty=False, level=0, indent='    ', newline=linesep):
        comment = self.getComment()
        if not pretty:
            return '<!--' + comment + '-->'
        else:
            result = ['<!--'] + list(comment.split(newline)) + ['-->']
            if len(result) > 3: 
                joinstr = newline+indent*level
            else: joinstr = ' '
            return joinstr.join(result)

    def __cmp__(self, other):
        return cmp(self.getComment(), other)

    def getComment(self):
        return self.comment.replace('<!--', '').replace('-->', '')
    def setComment(self, comment):
        self.comment = comment.replace('<!--', '').replace('-->', '')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class XMLNode(XMLNodeBase):
    """Simple class to build valid XML.
    Also has some basic access, query, and iteration methods.
    
    >>> node = XMLNode('mynode', 'mynamespace')
    >>> node.attrs['aname'] = 'avalue'
    >>> node.aname
    'avalue'
    >>> node += "\n"
    >>> node += "some cdata text \n"
    >>> node += "some more cdata text \n"
    >>> node += ('another_node', )
    >>> node += "\n"
    >>> node += ('third', 'namespace-for-third')
    >>> node += "\n"
    >>> node += ('forth', 'namespace-for-forth', 'four')
    >>> node += "\n"
    >>> print node
    <mynode xmlns="mynamespace" aname="avalue">
    some cdata text
    some more cdata text
    <another_node/>
    <third xmlns="namespace-for-third"/>
    <four:forth xmlns:four="namespace-for-forth"/>
    </mynode>
    """

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    #__slots__ = ['node', 'prefix', 'namespaces', 'elems', 'attrs', 'nodebuilder', 'softspace']
    nodebuilder = None
    default_node = None
    default_attributes = {}
    default_namespaces = XMLNamespaceMap()
    default_elements = []
    __xmlattrmixin__ = None

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Special Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __init__(self, node=None, namespace=None, prefix='', default_namespaces=None):
        if default_namespaces is not None: 
            self.namespaces = default_namespaces
        else: 
            self.namespaces = self.default_namespaces.copy()
        self.elems = self.default_elements[:]
        self.attrs = self.default_attributes.copy()
        self.node = node or self.default_node or self.__class__.__name__
        if namespace is None:
            self.namespace = (prefix, )
        else: 
            self.namespace = (prefix, namespace)
        self.softspace = 0 # for compatibility with file-like objects

    def __len__(self):
        return len(self.elems)

    def __getitem__(self, key, *args, **kw):
        """Returns a list of matching child elements of XMLNode.  See listItems."""
        if isinstance(key, _NodeKeyOrSlice):
            return self.elems.__getitem__(key, *args, **kw)
        else:
            return self.listItems(key, *args, **kw)
    def __setitem__(self, key, *args, **kw):
        """Sets child element at self.elem[key] = value."""
        if isinstance(key, _NodeKeyOrSlice):
            return self.elems.__setitem__(key, *args, **kw)
        else:
            raise TypeError, "Cannot set node elemenets with non integer key item operations"
    def __delitem__(self, key, *args, **kw):
        """Removes all matching child elements of XMLNode.  See delItems."""
        if isinstance(key, _NodeKeyOrSlice):
            return self.elems.__delitem__(key, *args, **kw)
        else:
            self.delItems(key, *args, **kw)

    def __contains__(self, key, *args, **kw):
        """Returns True if key is a child element of XMLNode.  See hasItem."""
        if isinstance(key, _NodeKeyOrSlice):
            return self.elems.__contains__(key, *args, **kw)
        else:
            return self.hasItem(key, *args, **kw)

    def __iadd__(self, other):
        """Adds an element to XMLNode.  Returns self.  See addItem."""
        self.addItem(other)
        return self

    def __add__(self, other):
        """Adds an element to XMLNode.  Returns node or self.  See addItem."""
        return self.addItem(other)

    def __iter__(self):
        """Returns an iterator of child elements."""
        return iter(self.elems)

    def __repr__(self):
        return '''<%s (%r, %r, %r)>''' % (self.__class__.__name__, self.node, self.namespace, self.prefix)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def addAttr(self, *args, **kw):
        """Adds attributes to XMLNode."""
        if args: self.attrs.update(dict(args))
        if kw: self.attrs.update(kw)
        return self

    def addData(self, cdata):
        """Adds a child cdata to XMLNode."""
        if cdata is not None:
            self.elems.append(cdata)
        return self

    def addComment(self, comment, *args, **kw):
        if comment is not None:
            self.elems.append(XMLComment(comment, *args, **kw))
        return self

    def addExplicit(self, *args, **kw):
        self.elems.append(XMLExplicit(*args, **kw))
        return self

    def addRaw(self, arg0, *args, **kw):
        if not (args or kw) and isinstance(arg0, XMLNodeBase):
            self.elems.append(arg0)
            return arg0
        else:
            return self.addExplicit(arg0, *args, **kw)

    def addText(self, *args, **kw): 
        """See addData."""
        return self.addData(*args, **kw)

    def insertData(self, idx, cdata):
        if cdata is not None:
            self.elems.insert(idx, cdata)
        return self

    def insertText(self, *args, **kw): 
        """See insertData."""
        return self.insertData(*args, **kw)

    def write(self, data):
        """For use in conjunction with file-like uses.

        >>> node = XMLNode('mynode', 'mynamespace')
        >>> print >> node
        >>> print >> node, 'some cdata'
        >>> node.toXML()
        '<mynode xmlns="mynamespace">\\nsome cdata\\n</mynode>'
        """
        self.addData(data)

    def addNode(self, arg0, *args, **kw):
        """Adds a child node to XMLNode."""
        if arg0 is None:
            return None
        self.softspace = 0
        result = self._makeNode(arg0, *args, **kw)
        self.elems.append(result)
        return result

    def insertNode(self, idx, arg0, *args, **kw):
        if arg0 is None:
            return None
        result = self._makeNode(arg0, *args, **kw)
        self.elems.insert(idx, result)
        return result

    def addItem(self, elem):
        """Adds a child element to XMLNode.
        Item is considered cdata if it is of string type, 
        or a node, otherwise."""
        if isinstance(elem, basestring):
            return self.addData(elem)
        elif isinstance(elem, XMLNodeBase):
            # For elements that are prebuilt
            self.elems.append(elem)
            return elem
        else: 
            # For building from tuples and lists
            return self.addNode(*elem)

    def insertItem(self, idx, elem):
        if isinstance(elem, basestring):
            return self.insertData(elem)
        elif isinstance(elem, XMLNodeBase):
            # For elements that are prebuilt
            self.elems.insert(idx, elem)
            return elem
        else: 
            # For building from tuples and lists
            return self.insertNode(*elem)

    def setxmlns(self, *args, **kw):
        return self.namespaces.setxmlns(*args, **kw)

    #~ iteration over elements ~~~~~~~~~~~~~~~~~~~~~~~~~~

    def enumData(self, match=None):
        """Returns a generator to iterate through the matching data indices in XMLNode"""
        if match is None: match = Any
        elif callable(match): match = MatchObj(match)
        idx = 0
        for each in self.elems:
            if isinstance(each, basestring):
                if match == each:
                    yield idx, each
            idx += 1

    def popData(self, match=None, **kw):
        idxList, result = [], []
        for idx, item in self.enumData(match, **kw):
            idxList.append(idx)
            result.append(item)
        map(self.elems.__delitem__, idxList[::-1])
        return result

    def iterData(self, match=None):
        """Returns a generator to iterate through the matching data in XMLNode"""
        if match is None: match = Any
        elif callable(match): match = MatchObj(match)
        for each in self.elems:
            if isinstance(each, basestring):
                if match == each:
                    yield each

    def listData(self, *args, **kw):
        """Returns a list of matching data in XMLNode"""
        return [x for x in self.iterData(*args, **kw)]

    def delData(self, *args, **kw):
        idxList = [x[0] for x in self.enumData(*args, **kw)]
        map(self.elems.__delitem__, idxList[::-1])

    def data(self, joinstr=''):
        return joinstr.join(map(type(joinstr), self.iterData(None)))

    def hasData(self, *args, **kw):
        """Returns True if data is in XMLNode"""
        try:
            self.iterData(*args, **kw).next()
            return True
        except StopIteration:
            return False

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def enumComments(self, match=None):
        """Returns a generator to iterate through the matching comments indices in XMLNode"""
        if match is None: match = Any
        elif callable(match): match = MatchObj(match)
        idx = 0
        for each in self.elems:
            if isinstance(each, XMLComment):
                if match == each:
                    yield idx, each
            idx += 1

    def popComments(self, match=None, **kw):
        idxList, result = [], []
        for idx, item in self.enumComments(match, **kw):
            idxList.append(idx)
            result.append(item)
        map(self.elems.__delitem__, idxList[::-1])
        return result

    def iterComments(self, match=None):
        """Returns a generator to iterate through the matching comments in XMLNode"""
        if match is None: match = Any
        elif callable(match): match = MatchObj(match)
        for each in self.elems:
            if isinstance(each, XMLComment):
                if match == each:
                    yield each

    def listComments(self, *args, **kw):
        """Returns a list of matching comments in XMLNode"""
        return [x for x in self.iterComments(*args, **kw)]

    def delComments(self, *args, **kw):
        idxList = [x[0] for x in self.enumComments(*args, **kw)]
        map(self.elems.__delitem__, idxList[::-1])

    def comments(self, joinstr=''):
        return joinstr.join(map(type(joinstr), self.iterComments(None)))

    def hasComments(self, *args, **kw):
        """Returns True if comments is in XMLNode"""
        try:
            self.iterComments(*args, **kw).next()
            return True
        except StopIteration:
            return False

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def enumNodes(self, *args, **kw):
        """Returns a generator to iterate through the matching child node indicies of XMLNode.
        obj.enumNodes(node=Any, namespace=Any, prefix=Any)"""
        match = makeNodeMatcher(*args, **kw)
        idx = 0
        for each in self.elems:
            if not isinstance(each, basestring):
                if match(each):
                    yield idx, each
            idx += 1

    def popNodes(self, *args, **kw):
        idxList, result = [], []
        for idx, item in self.enumNodes(*args, **kw):
            idxList.append(idx)
            result.append(item)
        map(self.elems.__delitem__, idxList[::-1])
        return result

    def iterNodes(self, *args, **kw):
        """Returns a generator to iterate through the matching child nodes of XMLNode.
        obj.iterNodes(node=Any, namespace=Any, prefix=Any)"""
        match = makeNodeMatcher(*args, **kw)
        for each in self.elems:
            if not isinstance(each, basestring):
                if match(each):
                    yield each

    def listNodes(self, *args, **kw):
        """Returns a list of matching child nodes of XMLNode"""
        return [x for x in self.iterNodes(*args, **kw)]

    def delNodes(self, *args, **kw):
        """Removes all matching child nodes of XMLNode"""
        idxList = [x[0] for x in self.enumNodes(*args, **kw)]
        map(self.elems.__delitem__, idxList[::-1])

    def hasNode(self, *args, **kw):
        """Returns True if elem is a child node of the XMLNode"""
        try:
            self.iterNodes(*args, **kw).next()
            return True
        except StopIteration:
            return False

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def enumItems(self, key=None, **kw):
        """Returns a generator to iterate through the matching child element indicies of XMLNode"""
        if key is None:
            return xrange(0, len(self.elems))
        elif isinstance(key, tuple):
            return self.enumNodes(*key, **kw)
        else:
            return self.enumData(key, **kw)

    def popItems(self, key=None, **kw):
        idxList, result = [], []
        for idx, item in self.enumItems(key, **kw):
            idxList.append(idx)
            result.append(item)
        map(self.elems.__delitem__, idxList[::-1])
        return result

    def iterItems(self, key=None, **kw):
        """Returns a generator to iterate through the matching child elements of XMLNode"""
        if key is None:
            return iter(self.elems)
        elif isinstance(key, tuple):
            return self.iterNodes(*key, **kw)
        else:
            return self.iterData(key, **kw)

    def listItems(self, *args, **kw):
        """Returns a list of matching child elements of XMLNode"""
        return [x for x in self.iterItems(*args, **kw)]

    def delItems(self, key, **kw):
        """Removes all matching child elements of XMLNode"""
        if key is None:
            del self.elems[:]
        elif isinstance(key, tuple):
            self.delNodes(*key, **kw)
        else:
            self.delData(key, **kw)

    def hasItem(self, elem=None, **kw):
        """Returns True if elem is a child element of the XMLNode"""
        if elem is None:
            for i in self.iterItems(None, **kw):
                return True
            return False
        elif isinstance(elem, (int, long)):
            del self.elems[elem]
        elif isinstance(elem, tuple):
            return self.hasNode(*elem, **kw)
        else:
            return self.hasData(*elem, **kw)

    #~ namespace property ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getNamespace(self):
        """Returns the namespace of the XMLNode"""
        return self.namespaces.xmlns(self.prefix or '')
    def setNamespace(self, value):
        """Sets the namespace of the XMLNode"""
        if isinstance(value, tuple):
            if len(value) == 1:
                self.prefix, namespace = value[0] or '', None
            else:
                self.prefix, namespace = value[0] or '', value[1]
        else:
            self.prefix, namespace = self.prefix or '', value
        if namespace is not None:
            self.namespaces.setxmlns(self.prefix, namespace)
    def delNamespace(self):
        """Removes the namespace of the XMLNode"""
        try: del self.namespaces[self.prefix or '']
        except KeyError: pass
    namespace = property(getNamespace, setNamespace, delNamespace)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def toXML(self, pretty=False, level=0, indent='    ', newline=linesep):
        """Converts the XMLNode to valid XML."""
        result = ['<']
        if self.prefix:
            nodename = self.prefix + ':' + self.node
        else: nodename = self.node
        result = ['<' + nodename]

        result.append(self.namespaces.toXML())

        for name, value in self.attrs.iteritems():
            result.append(' %s=%s' % (name, xmlquoteattr(value or "")))

        if self.elems:
            result.append('>')
            result.extend(self._elemsToXML(pretty, level+1, indent, newline))
            if pretty: result.append(newline + indent * level)
            result.append('</%s>' % nodename)
        else:
            result.append('/>')
        return ''.join(result)  

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Protected Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _getNodeFactory(self, *args, **kw):
        nodebuilder = kw.pop('nodebuilder', self.__class__)
        return nodebuilder, args, kw

    def _makeNode(self, arg0, *args, **kw):
        nodebuilder = getattr(arg0, 'asXMLNode', None)
        if nodebuilder is not None:
            return nodebuilder()
        else:
            kw['default_namespaces'] = self.namespaces.newChain()
            nodebuilder, args, kw = self._getNodeFactory(arg0, *args, **kw)
            return nodebuilder(*args, **kw)

    def _elemsToXML(self, pretty, level, indent, newline):
        """Converts child elements of XMLNode to valid XML."""
        if pretty: prettyIndent = newline + indent * level
        result = []
        wasText = False
        for elem in self.elems:
            if isinstance(elem, basestring):
                if pretty and not wasText: result.append(prettyIndent)
                elem = xmlescape(elem)
                if pretty: 
                    elem = elem.replace(newline, prettyIndent)
                result.append(elem)
                wasText = True
            else: 
                if pretty: result.append(prettyIndent)
                result.append(elem.toXML(pretty, level, indent, newline))
                wasText = False
        return result

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ xmlBuilder cooperation
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

try: import xmlBuilder
except ImportError: pass
else:
    class NodeXML(XMLNode, xmlBuilder.ElementBase):
        """An inherited bridge between ElementBase interface and XMLNode"""
        def __init__(self, elemBuilder, parent, node, attributes, namespacemap):
            prefix = namespacemap.prefix(node[0])
            if node[0] in namespacemap: xmlns, nodename = node
            elif namespacemap.nextmap is None: xmlns, nodename = node
            else: xmlns, nodename = None, node[1]
            XMLNode.__init__(self, nodename, xmlns, prefix, default_namespaces=namespacemap)

            for key, value in attributes.iteritems():
                if isinstance(key, tuple):
                    try:
                        prefix = namespacemap.prefix(key[0])
                        if not prefix: key = key[1]
                        else: key = ':'.join((prefix, key[1]))
                    except KeyError: key = key[1]
                self.attrs[key] = value

        def xmlAddElement(self, elemBuilder, node, obj, srcref): 
            if obj is not None: 
                self.elems.append(obj)
        def xmlAddData(self, elemBuilder, data, srcref): 
            if data is not None: 
                self.elems.append(data)
        def xmlAddComment(self, elemBuilder, comment):
            if comment is not None: 
                self.elems.append(XMLComment(comment))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    class NodeXMLAdaptor(xmlBuilder.ElementBase):
        """An external adaptor to bridge between ElementBase interface and XMLNode"""
        nodebuilder = XMLNode

        def __init__(self, elemBuilder, parent, node, attributes, namespacemap, nodebuilder=XMLNode):
            prefix = namespacemap.prefix(node[0])
            if node[0] in namespacemap: xmlns, nodename = node
            elif namespacemap.nextmap is None: xmlns, nodename = node
            else: xmlns, nodename = None, node[1]
            nodebuilder = nodebuilder or self.nodebuilder
            self.result = nodebuilder(nodename, xmlns, prefix, default_namespaces=namespacemap)

            for key, value in attributes.iteritems():
                if isinstance(key, tuple):
                    try:
                        prefix = namespacemap.prefix(key[0])
                        if not prefix: key = key[1]
                        else: key = ':'.join((prefix, key[1]))
                    except KeyError: key = key[1]
                self.result.attrs[key] = value

        def xmlAddElement(self, elemBuilder, node, obj, srcref): 
            self.result.elems.append(obj)
        def xmlAddData(self, elemBuilder, data, srcref): 
            self.result.elems.append(data)
        def xmlAddComment(self, elemBuilder, comment):
            self.result.elems.append(XMLComment(comment))
        def xmlGetElement(self, elemBuilder): 
            return self.result
        def toXML(self, *args, **kw):
            return self.result.toXML()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    class XMLNodeFactory(object):
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #~ Constants / Variables / Etc. 
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        nodebuilder = XMLNode
        xmladaptor = NodeXMLAdaptor

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #~ Public Methods 
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        def __init__(self, nodebuilder=None, xmladaptor=None):
            self.nodebuilder = nodebuilder or self.nodebuilder
            self.xmladaptor = xmladaptor or self.xmladaptor

        def __call__(self, elemBuilder, parent, node, attributes, namespacemap):
            return self.buildNode
                
        def buildNode(self, *args, **kw):
            return self.xmladaptor(nodebuilder=self.nodebuilder, *args, **kw)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    class Producer(xmlBuilder.XMLBuilder): 
        """An implementation of XMLBuilder that creates xmlnodes from an XML stream."""
        ElementFactory = NodeXMLAdaptor
        def _getElementFactory(self, elemBuilder, parent, node, attributes, namespacemap):
            return self.xmlClassFactory

    def asXMLNode(xmlOrNode):
        if isinstance(xmlOrNode, XMLNode):
            return xmlOrNode
        else:
            return Producer().parse(xmlOrNode)
    XMLNode.asXMLNode = staticmethod(asXMLNode)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Testing 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    import StringIO
    root = XMLNode('root', 'MyRootNamespace')
    root += 'Some cdata'
    root += ('subelem',)
    root += 'More data'
    root += ('element',)
    root += 'anotherelem', 'SubNamespace'
    anotherelem = root[-1]
    anotherelem.attrs['myattr'] = 'a value'
    anotherelem += 'some text'

    print
    print "Plain::"
    print root.toXML()
    print

    print
    print "Pretty::"
    print root.toXML(True)
    print

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    someXML = root.toXML(True)
    xml = Producer().parse(someXML)
    assert xml.toXML() == someXML

    someXMLFile = StringIO.StringIO(someXML)
    xml = Producer().parseFile(someXMLFile)
    assert xml.toXML() == someXML

