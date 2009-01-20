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

import os
import sys
import webbrowser

import wx

from TG.skinning.toolkits.wx import wxSkinModel
from TG.guiTools.wx.listCtrl import ListItem
from TG.guiTools.wx.treeCtrl import TreeItem

import rssNews

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Skin Model
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class RSSNewsSkinModel(wxSkinModel):
    xmlSkinRef = '/skins/main.skin'

    newsRoot = rssNews.Collection('News Sites', [
        rssNews.Collection('TechGame Blogs', [
            rssNews.Site('Apple Hot News', 'http://www.apple.com/main/rss/hotnews/hotnews.rss'),
            rssNews.Site('Smalltalk Tidbits, Industry Rants', 'http://www.cincomsmalltalk.com/rssBlog/rssBlogView.xml'),
            ]),
        rssNews.Collection('TechGame Framework', [
            rssNews.Site('TG Timeline', 'http://www.techgame.net/projects/Framework/timeline?daysback=5&amp;max=50&amp;format=rss'),
            rssNews.Site('TG Tickets', 'http://www.techgame.net/projects/Framework/report/3?format=rss&USER=anonymous'),
            ]),
        rssNews.Collection('Python News', [
            rssNews.Site('Daily Python-URL', 'http://www.pythonware.com/daily/rss2.xml'),
            rssNews.Site('PyPi', 'http://python.org/pypi?:action=rss'),
            #rssNews.Site('', ''),
            ]),
        ])

    _currentSite = None
    _currentEntry = None

    def onSkinModelComplete(self, *args):
        if not rssNews.feedparser:
            message = rssNews.download_info.replace('\n', os.linesep)
            result = wx.MessageBox(message, style=wx.YES_NO|wx.YES_DEFAULT|wx.ICON_ERROR)
            if result == wx.YES:
                webbrowser.open('http://www.feedparser.org/')
            sys.exit()

        self.siteTree.DeleteAllItems()
        rootItem = self.newsRoot.addTo(self, None)
    
    def refresh(self):
        self.populate(refresh=True)

    def addSiteCollection(self, siteCollection, tiParent):
        ti = TreeItem()
        ti.SetText(siteCollection.getTitle())
        ti.addToTree(self.siteTree, tiParent)
        ti.site = siteCollection

        for subsite in siteCollection.getChildSites():
            subsite.addTo(self, ti)

        self.siteTree.Expand(ti.GetTreeId())
        return ti

    def addSite(self, site, tiParent):
        ti = TreeItem()
        ti.SetText(site.getTitle())
        ti.addToTree(self.siteTree, tiParent)
        ti.installItemModel(self.siteTree)
        ti.site = site
        return ti

    def populateFromEvt(self, evt):
        evtObj = evt.GetEventObject()
        data = evtObj.GetPyData(evtObj.GetSelection())

        self.populate(data.site)

    def populate(self, site=None, refresh=False):
        if site is None:
            site = self._currentSite
        else:
            self._currentSite = site

        if site is None:
            return

        wx.BeginBusyCursor()
        try:
            rss = self._currentSite.load(refresh=refresh)
            self.setSelectedEntry(None)

            self.newsList.DeleteAllItems()
            newsList = self.newsList
            for idx, entry in enumerate(rss.entries):
                newsList.InsertStringItem(idx, entry.title)
                newsList.SetStringItem(idx, 1, entry.get('category', ''))
                newsList.SetStringItem(idx, 2, entry.get('author', ''))
                newsList.setItemPyData(idx, entry)
        finally:
            wx.EndBusyCursor()

    def onAddSite(self, evt):
        # TODO: Implement site Add/Remove and saving
        wx.MessageBox('Adding of sites has not yet been implemented.')

    def onShowDetails(self, evt):
        idx = evt.GetIndex()
        if idx < 0:
            return 

        newsList = evt.GetEventObject()
        entry = newsList.getItemPyData(idx)

        self.setSelectedEntry(entry)

    def setSelectedEntry(self, entry=None):
        self._currentEntry = entry
        if entry is None:
            self.detailsSash.Show(False)
            self.detailTitle.SetLabel('')
            self.details.SetPage('')
        else:
            self.detailsSash.Show(True)
            self.detailTitle.SetLabel(entry.title)
            try:
                text = entry.summary
            except AttributeError:
                text = os.linesep.join([('%s: %r' % i)[:60] for i in entry.items()])
            self.details.SetPage(text)

    def onFollowLink(self, url=None):
        if url is None:
            if self._currentEntry:
                url = self._currentEntry.link
        if url:
            webbrowser.open(url)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    RSSNewsSkinModel().skinModel()

