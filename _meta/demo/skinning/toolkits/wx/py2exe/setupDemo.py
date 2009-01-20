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

from distutils.core import setup
import py2exe
import modulefinder
import TG

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

for subpath in TG.__path__:
    modulefinder.AddPackagePath("TG", subpath)

py2exeOptions = dict(
    packages = ["TG.skinning", "TG.common"],
    ignores = [],
    includes = ['encodings', 'encodings.ascii', 'encodings.latin_1', 'encodings.utf_8', 'encodings.utf_16'],
    excludes = [],
    dll_excludes = [],
    compressed = True,
    )

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    setup(
        windows=["demo.py"],
        #console=["demo.py"],
        options = {
            "py2exe": py2exeOptions,
            },
        data_files = [
            ('.', ['fileExplorer.skin', 'hello.py'])
            ],
        )

