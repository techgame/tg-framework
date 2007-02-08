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

from code import compileWithFileAndLine

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def compileTraceSrcref(srcref, code, mode='eval'):
    """Compiles python statement to add srcref's filename and linenumber directly into the traceback"""
    return compileWithFileAndLine(code, mode, *srcref)

def traceSrcrefExec(srcref, code, **kw):
    """Executes the code in a context containting the filename and linenumber -- very useful for tracebacks"""
    code = compileTraceSrcref(srcref, code, 'exec')
    exec code in kw
    return kw

def traceSrcrefEval(srcref, code, **kw):
    """Evaluates the code in a context containting the filename and linenumber -- very useful for tracebacks"""
    code = compileTraceSrcref(srcref, code, 'eval')
    return eval(code, {}, kw)

