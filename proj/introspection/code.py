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

import new

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Constants / Variables / Etc. 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

codeAttributeNames = [ 
    # note that the order is determined by new.code() method
    'co_argcount',
    'co_nlocals',
    'co_stacksize',
    'co_flags',
    'co_code',
    'co_consts',
    'co_names',
    'co_varnames',
    'co_filename',
    'co_name',
    'co_firstlineno',
    'co_lnotab',
    'co_freevars',
    'co_cellvars',
    ]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def codeObjAsData(codeObj):
    global codeAttributeNames
    return dict([(n, getattr(codeObj, n)) for n in codeAttributeNames])
def codeObjFromData(codeData):
    global codeAttributeNames
    return new.code(*[codeData[n] for n in codeAttributeNames])

def replaceCodeItems(codeObj, **kw):
    global codeObjAsData, codeObjFromData
    data = codeObjAsData(codeObj)
    data.update(kw)
    return codeObjFromData(data)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CodeToken(object):
    codeData = None

    def __init__(self, codeObj=None):
        if codeObj is not None:
            self.setCodeObj(codeObj)

    def replace(self, **kw):
        self.codeData.update(kw)

    def __getitem__(self, item):
        return self.codeData[item]
    def __setitem__(self, item, value):
        self.codeData[item] = value

    def getCodeObj(self):
        return self.codeObjFromData(self.codeData)
    def setCodeObj(self, codeObj):
        self.codeData = self.codeObjAsData(codeObj)
        return self.codeData

    codeObjAsData = staticmethod(codeObjAsData)
    codeObjFromData = staticmethod(codeObjFromData)
    replaceCodeItems = staticmethod(replaceCodeItems)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

newlineMax = 250 # let's not push it -- 250 is a good marker
newlineBlock = '\n'* (newlineMax-1) + 'pass\n'
def compileWithFileAndLine(source, mode, filename, lineNumber=None, offset=0):
    if lineNumber is not None:
        lineNumber += offset

    # manage the line numbers
    if lineNumber and mode == 'exec':
        # we use a trick for exec so that methods get the correct line
        # number.  Prepend the corrent number of newlines.  Ugly, huh? ;) 
        # Update: Due to python bug #1512814, it appears that our line numbers
        # will be off if they have more than 255 blank lines!
        nlBlock = newlineBlock
        m, r = divmod(lineNumber-1, newlineMax)
        blanks = m*nlBlock + nlBlock[:r]
        source = blanks + source
        lineNumber = None

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    code = compile(source, filename or '', mode)

    if lineNumber: # lineNumber is None if it hit the exec block above
        # for eval, we replace the code's line number, because it ignores the
        # newlines from the exec trick above
        global replaceCodeItems
        code = replaceCodeItems(code, co_firstlineno=lineNumber)

    return code

