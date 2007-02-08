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

try: 
    import cStringIO as StringIO
except ImportError:
    import StringIO

from TG.introspection import getFrameFileAndLine
from TG.w3c.xmlParserContext import ParseContext as ParseContextBase

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SkinParseContext(ParseContextBase):
    uriNode = None
    def getURINode(self):
        return self.uriNode
    def setURINode(self, uriNode):
        self.uriNode = uriNode
        if uriNode is not None:
            self.setURI(uriNode.asResolvableURI())

    def __repr__(self):
        return "<%s.%s in \"%s\":%d>" % (self.__class__.__module__, self.__class__.__name__, self.getFilename(), self.getLineOffset())
    def __str__(self): 
        return self.getSource()
    def __unicode__(self): 
        return self.getSource()

    def getSource(self):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def openFile(self, mode='rb'):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))


class URISkinParseContext(SkinParseContext):
    def __init__(self, uriNode):
        self.setURINode(uriNode)
        self.setFilename(uriNode.getPath())

    def getSource(self):
        sourceFile = self.openFile()
        try:
            source = sourceFile.read()
        finally:
            sourceFile.close()
        return source
    def openFile(self, mode='rb'):
        return self.uriNode.open(mode)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class XMLSkinParseContext(SkinParseContext):
    def __init__(self, xmlSource, uriNode=None, getFrameContext=True):
        self.setSource(xmlSource)
        self.setURINode(uriNode)

        if getFrameContext:
            filename, lineNumber, fromEnd = getFrameFileAndLine(1)
            if fromEnd: 
                lineNumber -= xmlSource.count('\n')
            self.setFilenameAndOffset(filename, lineNumber-1)

    def fromSourceData(klass, xmlSource, uri=None):
        return klass(xmlSource, uri, False)
    fromSourceData = classmethod(fromSourceData)

    def getSource(self):
        return self.xmlSource
    def setSource(self, xmlSource):
        self.xmlSource = xmlSource

    def openFile(self, mode='rb'):
        return StringIO.StringIO(self.getSource())

XMLSkin = XMLSkinParseContext

