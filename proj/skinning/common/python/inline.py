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

import re
from _baseElements import PythonSkinElement, PassThroughElement

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

inlineCodeTemplate = """if 1:%s"""

class InlineMixin(object):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    re_blankLineComments = re.compile('^\s*#.*$', re.MULTILINE)
    codeTemplate = inlineCodeTemplate
    codeTemplateLineOffset = 0
    _ctxHostCodeNames = ()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Definitions 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _executeContent(self, elemBuilder, content):
        if not content: 
            return

        content = self.re_blankLineComments.sub('\n', content).rstrip()
        if not content.strip(): 
            return
        elif not content[0].isspace() and ('\n' not in content):
            # handle single inline
            content = '    '+content

        source = self._applyCodeTemplate(content)
        code = self.compile(source, lineOffset=self.codeTemplateLineOffset)
        self.execute(code)

    def _applyCodeTemplate(self, content):
        return self.codeTemplate % (content,)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def setInitialContext(self):
        result = PythonSkinElement.setInitialContext(self)
        self.setCtxHostCode()
        if self.hasSetting('ctxcode', 1):
            self.setCtxCode()
        return result

    def _unravelCtxVars(self):
        result = PythonSkinElement._unravelCtxVars(self)
        if self.hasSetting('ctxcode', 1):
            self.delCtxCode()

    def setCtxHostCode(self):
        ctx = self.getContext()
        module = self.getExecModule()
        for name in self._ctxHostCodeNames:
            setattr(ctx, name, module)

    def setCtxCode(self):
        owner, name = self.getSettingAsAddress('ctxcode', ctx=self.getParentContext())
        setattr(owner, name, self.getExecModule())
    def delCtxCode(self):
        owner, name = self.getSettingAsAddress('ctxcode', ctx=self.getParentContext())
        delattr(owner, name)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class InlinePythonSkinElement(InlineMixin, PythonSkinElement):
    pass

class InlinePythonSkinElementPassThrough(InlineMixin, PassThroughElement):
    pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class inline(InlinePythonSkinElementPassThrough):
    pass

