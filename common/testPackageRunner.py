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

import os, sys
import types
import unittest

from TG.common import path

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = ['TestResult', 'TestCase', 'TestSuite', 'TextTestRunner',
           'TestLoader', 'FunctionTestCase', 'main', 'defaultTestLoader']

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TestResult = unittest.TestResult
TestCase = unittest.TestCase
FunctionTestCase = unittest.FunctionTestCase
TextTestRunner = unittest.TextTestRunner

class TestLoader(unittest.TestLoader):
    def loadTestsFromModule(self, module):
        tests = []
        for name in dir(module):
            obj = getattr(module, name)
            atest = self.loadTestFromModuleVariable(name,obj)
            if atest is not None:
                tests.append(atest)
        return self.suiteClass(tests)

    def loadTestFromModuleVariable(self, name, obj):
        if isinstance(obj, (type, types.ClassType)):
            if issubclass(obj, TestCase):
                return self.loadTestsFromTestCase(obj)
            elif issubclass(obj, TestSuite):
                return obj()
        return None

    def loadTestsFromTestCase(self, testCaseClass):
        """Return a suite of all tests cases contained in testCaseClass"""
        if issubclass(testCaseClass, TestSuite):
            raise TypeError("Test cases should not be derived from TestSuite. Maybe you meant to derive from TestCase?")
        testCaseNames = self.getTestCaseNames(testCaseClass)
        return self.suiteClass(map(testCaseClass, testCaseNames))

defaultTestLoader = TestLoader()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TestSuite(unittest.TestSuite):
    def __init__(self, *args, **kw):
        unittest.TestSuite.__init__(self, *args, **kw)
        if not args and not kw:
            self.generateTests()

    def generateTests(self):
        pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TestSuitePackage(TestSuite):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    testModulesPattern = 'test*.py'
    sortTestsUsing = cmp

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __init__(self, testdir, recurse=False, testLoader=defaultTestLoader):
        TestSuite.__init__(self)
        self.testdir = testdir
        self.recurse = recurse
        self.testLoader = testLoader
        self._findAllTests(testdir)

    def id(self):
        return "%s for %s" % (self.__class__, self.testdir)

    def _findAllTests(self, testdir):
        result = []

        sys.path.insert(0, testdir)
        for testmodule in testdir.files(self.testModulesPattern):
            try:
                testmodule = __import__(testmodule.name[:-3], {}, {}, None)
                result.append(self.testLoader.loadTestsFromModule(testmodule))
            except StandardError:
                sys.excepthook(*sys.exc_info())
        sys.path.pop(0)

        if self.recurse:
            for testpackage in testdir.dirs():
                result.append(self.__class__(testpackage, self.recurse, self.testLoader))

        result = filter(None, result)
        result.sort(self.sortTestsUsing)
        return self.addTests(result)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TestProgram(unittest.TestProgram):
    def __init__(self, module='__main__', defaultTest=None,
                 argv=None, testRunner=None, testLoader=defaultTestLoader):
        unittest.TestProgram.__init__(self, module, defaultTest, argv,
                testRunner, testLoader)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TestPackageProgram:
    """A command-line program that runs a package of tests; this is primarily
    for making test modules conveniently executable.  Implementation derived
    from unittest.TestProgram.
    """

    USAGE = """\
Usage: %(progName)s [options]

Options:
  -h, --help           Show this message
  -v, --verbose        Verbose output
  -q, --quiet          Minimal output
  -r <bool>, --recure=<bool>
                       Recurse subdirectories [default]

"""

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    packageSuiteClass = TestSuitePackage

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __init__(self, 
            testdir=os.getcwd(), 
            argv=sys.argv, 
            testRunner=None, 
            testLoader=defaultTestLoader):

        self.testdir = path.path(testdir)
        self.testRunner = testRunner
        self.testLoader = testLoader
        self.parseArgs(argv)
        self.createTests()
        self.runTests()

    def usageExit(self, msg=None):
        if msg: print msg
        print self.USAGE % {'progName': path.path(sys.argv[0]).name}
        sys.exit(2)

    def parseArgs(self, argv):
        import getopt
        try:
            self.verbosity = 1
            self.recurse = 1

            options, args = getopt.getopt(argv[1:], 'hHvqr:', 
                ['help','verbose','quiet','recurse='])
            for opt, value in options:
                if opt in ('-h','-H','--help'):
                    self.usageExit()
                elif opt in ('-q','--quiet'):
                    self.verbosity = 0
                elif opt in ('-v','--verbose'):
                    self.verbosity = 2
                elif opt in ('-r','--recurse'):
                    self.recurse = int(value)
        except getopt.error, msg:
            self.usageExit(msg)

    def createTests(self):
        self.test = self.packageSuiteClass(self.testdir, self.recurse, self.testLoader)

    def runTests(self):
        if self.testRunner is None:
            self.testRunner = unittest.TextTestRunner(verbosity=self.verbosity)
        result = self.testRunner.run(self.test)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

main = TestPackageProgram

