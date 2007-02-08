#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os
import sys
import traceback

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class GVIMTracebacks(object):
    def install(self):
        self._nextExceptHook = sys.excepthook
        sys.excepthook = self

    def uninstall(self):
        if sys.excepthook == self:
            sys.excepthook = self._nextExceptHook
            self._nextExceptHook = None

    def format(self, type_, value, tb):
        self._nextExceptHook(type_, value, tb)
        if value is None:
            exceptionName = type_
        else:
            exceptionName = type_.__name__
        info = traceback.format_exception_only(type_, value)[0][:-1]
        stack = traceback.extract_tb(tb)
        del tb

        errFilename = self.getFilename()
        self.createMessageFormat(errFilename, exceptionName, info, stack)
        self.startEdititor(errFilename)

    __call__ = format

    def getFilename(self):
        return '%s.tb' % (sys.argv[0], )

    def createMessageFormat(self, errFilename, exceptionName, info, stack):
        # write the error to the file
        outfile = open(errFilename, 'w')
        filename, lineno = '', 0
        for (filename, lineno, method, code) in stack:
            print >> outfile, '%s:%d: %s -- in %s: %s' % (filename, lineno, exceptionName, method, code)
        print >> outfile, '%s:%d: %s' % (filename, lineno, info)
        outfile.close()

    def startEdititor(self, errFilename):
        # start gvim at the filename
        dirname = os.path.abspath('.')
        cmd = 'gvim --remote-send ":cd %s<CR>:cf %s<CR>:botright cwindow<CR>:clast<CR>"' % (dirname, os.path.abspath(errFilename))
        print "Run:", 'gvim -q "%s" +copen +clast' % (errFilename,)
        os.system(cmd)

def install():
    GVIMTracebacks().install()

