
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

import urllib2

try:
    import feedparser
except ImportError:
    feedparser = None
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Constants / Variables / Etc. 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

download_info = """\
RSS Engine was not found.  ('import feedparser' failed.)
Please download and install feedparser from http://www.feedparser.org/

Would you like to open that page now?"""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ News Sources
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SourceAbstract(object):
    title = '<an RSS Source>'
    rss = None

    def load(self, refresh=False):
        raise NotImplementedError('Subclass Responsibility') 

    def getTitle(self):
        return self.title

    def addTo(self, host, *args, **kw):
        raise NotImplementedError('Subclass Responsibility') 

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Collection(SourceAbstract):
    def __init__(self, title, sites):
        self.title = title
        self.sites = list(sites)

    def load(self, *args, **kw):
        return self.getDefaultSite().load(*args, **kw)

    def getDefaultSite(self):
        return self.sites[0]

    def getChildSites(self):
        return self.sites

    def addTo(self, host, *args, **kw):
        return host.addSiteCollection(self, *args, **kw)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Source(SourceAbstract):
    title = '<an RSS Source>'
    rss = None

    def load(self, refresh=False):
        if refresh or self.rss is None:
            self.rss = self.parseRSS()
        return self.rss

    def parseRSS(self):
        xmlData = self.open()
        return feedparser.parse(xmlData)

    def open(self):
        raise NotImplementedError('Subclass Responsibility') 

    def addTo(self, host, *args, **kw):
        return host.addSite(self, *args, **kw)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Site(Source):
    url = None
    auth = None

    def __init__(self, titleOrURL, url=NotImplemented):
        if url is NotImplemented:
            self.url = titleOrURL
        else:
            self.title = titleOrURL
            self.url = url

    def setBasicAuthorization(self, username, password):
        self.auth = "Basic " + ':'.join((username, password)).encode('base64')

    def open(self):
        request = urllib2.Request(self.url)
        if self.auth is not None:
            request.add_header("Authorization",  self.auth)
        return urllib2.urlopen(request)

