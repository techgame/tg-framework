#!/usr/bin/env python
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##~ Copyright (C) 2002-2004  TechGame Networks, LLC.
##~ 
##~ This library is free software; you can redistribute it and/or
##~ modify it under the terms of the BSD style License as found in the 
##~ LICENSE file included with this distribution.
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""TechGame Framework CSS Parser and Engine"""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from distutils.core import setup

import packageDefinitions

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Constants / Variables / Etc. 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

keywords = ["CSS", "HTML", "XML"]

TroveClassifiers = [
    'Development Status :: 3 - Alpha',
    'License :: OSI Approved :: BSD License',
    'Intended Audience :: Developers',

    'Environment :: Web Environment',
    'Operating System :: OS Independent',

    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Text Processing :: Markup :: HTML',
    'Topic :: Text Processing :: Markup :: CSS',
    'Topic :: Text Processing :: Markup :: XML',
    ],

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PackageInfo = dict(
    name= "TG-CSS-Tools", version= "1.0a2(svn)",

    url= "http://techgame.net/projects/Framework/wiki/",
    download_url= "http://techgame.net/projects/Framework/wiki/MilestoneRelease1.0a2",

    author= "TechGame Networks, LLC.",
    author_email= "framework@techgame.net",
    license= 'OSI Certified Open Source BSD-style. See http://techgame.net/projects/Framework/wiki/License for more details.',
    description= __doc__.split('\n',1)[0],
    long_description= __doc__,

    platforms= "OS Independent", 
    classifiers= TroveClassifiers,
    keywords= keywords,

    data_files = [
        ('doc/site-packages/TG', ['README.txt', 'LICENSE.txt'])
        ],

    package_dir= {'TG': 'proj'},
    packages= packageDefinitions.base,
    py_modules=[
        "TG.w3c.css", 
        "TG.w3c.cssParser", 
        "TG.w3c.cssDOMElementInterface", 

        # To allow for testing:
        "TG.common.path", 
        "TG.common.testPackageRunner", 
        ],

    options={
        "bdist": {
            "formats":"zip,wininst",
        },
        "sdist": {
            "formats":"zip,gztar",
            "template":"css.manifest.in",
            "manifest":"css.manifest",
        },
    },
    )

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    setup(**PackageInfo)

