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

from xml.parsers import expat as _expat

from TG.introspection.stack import traceSrcrefExec, traceSrcrefEval

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Parse Context and Parse Command
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ParseContextBase(object):
    def getURI(self):
        return self.getFilename()
    def getEncoding(self):
        return None
    def getFilenameAndOffset(self):
        return (self.getFilename(), self.getLineOffset())
    def getFilename(self):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def getLineOffset(self):
        return 0

class ParseContext(ParseContextBase):
    "A practical implementation of ParseContextBase"
    encoding = None
    uri = None
    filename = None
    lineOffset = 0

    def getURI(self):
        if self.uri is not None:
            return self.uri
        else:
            return self.getFilename()
    def setURI(self, uri):
        self.uri = uri

    def getEncoding(self):
        return self.encoding
    def setEncoding(self, encoding):
        self.encoding = encoding

    def getFilename(self):
        return self.filename
    def setFilename(self, filename):
        self.filename = filename

    def getLineOffset(self):
        return self.lineOffset
    def setLineOffset(self, lineOffset=0):
        self.lineOffset = lineOffset

    def getFilenameAndOffset(self):
        return self.getFilename(), self.getLineOffset()
    def setFilenameAndOffset(self, filename, lineOffset=0):
        self.setFilename(filename)
        self.setLineOffset(lineOffset)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ParserCmdBase(object):
    encoding = None
    _parseContext = None
    _sourceFilename = None
    _sourceLineOffset = 0

    def __init__(self, host, xmlSource, parserInterface, parseContext):
        """Creates the Expat parser in a composed way.  

        parserInterface:
            'data': returns a callable that takes a string of the XML document
            'file': returns a callable that takes a file-like interface to the XML document
            'raw': returns the raw parser object
        """
        self.xmlSource = xmlSource

        if (parseContext is None) and isinstance(xmlSource, ParseContextBase):
            parseContext = xmlSource

        self.setContext(parseContext)
        self.parser = self._createParserOnHost(host, parserInterface)
        self.configureParser(parseContext, parserInterface)

    #~ Parse Context delegation ~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getContext(self):
        return self._parseContext
    def setContext(self, parseContext):
        self._parseContext = parseContext
        if parseContext is not None:
            self.setEncoding(parseContext.getEncoding())
            self.setSourceFilenameAndOffset(*parseContext.getFilenameAndOffset())

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getURI(self):
        parseContext = self.getContext()
        if parseContext:
            return parseContext.getURI()
        else:
            return None

    #~ cached variables ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getSourceFilename(self):
        return self._sourceFilename
    def getSourceLineOffset(self):
        return self._sourceLineOffset
    def getSourceFilenameAndOffset(self):
        return (self._sourceFilename, self._sourceLineOffset)
    def setSourceFilenameAndOffset(self, filename, lineOffset=0):
        self._sourceFilename = filename
        self._sourceLineOffset = lineOffset

    def getSourceLineNumber(self, offset=0):
        return self._sourceLineOffset + self.getParserLineNumber() + offset
    def getSourceFilenameAndLineNumber(self, offset=0):
        return (self.getSourceFilename(), self.getSourceLineNumber(offset))

    def getEncoding(self, default=None):
        return self.encoding
    def setEncoding(self, encoding):
        self.encoding = encoding

    #~ Parser supplied methods ~~~~~~~~~~~~~~~~~~~~~~~~~~

    def configureParser(self, parseContext):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

    def __call__(self, xmlSource):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

    def getParserLineNumber(self):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Expat XML Parser Cmd
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class AdvExpatError(_expat.ExpatError):
    def __init__(self, expatError, parseCmd):
        self.expatError = expatError
        self.srcref = parseCmd.getSourceFilenameAndLineNumber()

    def __str__(self):
        errMsg = str(self.expatError)
        errMsg =  errMsg[:errMsg.rfind(': line')]
        return '%s: in File "%s" line %s, column %s' % (errMsg, self.srcref[0], self.srcref[1], self.expatError.offset)

    def raiseFromSrc(self):
        global traceSrcrefExec
        traceSrcrefExec(self.srcref, 'raise xmlError', xmlError=self)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ExpatParserCmd(ParserCmdBase):
    def _createParserOnHost(self, host, parserInterface):
        encoding = self.getEncoding()
        parser = _expat.ParserCreate(encoding, host.seperator)
        parser.returns_unicode = encoding and (encoding.lower() != 'ascii')

        # hook the parse callbacks
        parser.buffer_text = True
        parser.StartElementHandler = self._dynamicCallTo(host._startElement)
        parser.EndElementHandler = self._dynamicCallTo(host._endElement)
        parser.CharacterDataHandler = self._dynamicCallTo(host._charData)
        parser.CommentHandler = self._dynamicCallTo(host._commentData)
        parser.StartNamespaceDeclHandler = self._dynamicCallTo(host._startNamespaceDeclHandler)
        parser.EndNamespaceDeclHandler = self._dynamicCallTo(host._endNamespaceDeclHandler)

        return parser

    def _dynamicCallTo(self, callback):
        if self.getContext() is None:
            return callback
        def dynStackCB(*args, **kw):
            global traceSrcrefEval
            srcref = self.getSourceFilenameAndLineNumber()
            return traceSrcrefEval(srcref, 'expatCB(*args, **kw)', args=args, kw=kw, expatCB=callback)
        return dynStackCB

    def __call__(self):
        try:
            if self._parserInterface == 'file':
                return self.parser.ParseFile(self.xmlSource)
            elif self._parserInterface == 'data':
                return self.parser.Parse(unicode(self.xmlSource), False)
            elif self._parserInterface == 'raw':
                return self.parser(self.xmlSource)
            else:
                raise ValueError('Invalid parserInterface: %r' % (self._parserInterface,))
        except _expat.ExpatError, err:
            AdvExpatError(err, self).raiseFromSrc()

    def getParserLineNumber(self):
        return self.parser.ErrorLineNumber

    def getParserColumnNumber(self):
        return self.parser.ErrorColumnNumber

    #~ parseContext ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def configureParser(self, parseContext, parserInterface):
        self._parserInterface = parserInterface
        uri = unicode(self.getURI() or u'')
        self.parser.SetBase(uri)

