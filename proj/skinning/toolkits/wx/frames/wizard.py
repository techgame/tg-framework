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

from dialog import *
import wx.wizard

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SkinWizard(wx.wizard.Wizard):
    _firstPage = None

    def RunWizard(self, firstPage=None):
        if firstPage is None:
            firstPage = self.GetFirstPage()
        self.update()
        return wx.wizard.Wizard.RunWizard(self, firstPage)

    def GetFirstPage(self):
        return self._firstPage
    def SetFirstPage(self, page):
        self._firstPage = page

    def update(self):
        page = self.GetCurrentPage() or self.GetFirstPage()
        nextButton = self.FindWindowById(wx.ID_FORWARD)
        nextButton.Enable(self.isNextEnabled(page))

        prevButton = self.FindWindowById(wx.ID_BACKWARD)
        prevButton.Enable(self.isPrevEnabled(page))

    def isPrevEnabled(self, page):
        if hasattr(page, 'isDynamic') and page.isDynamic():
            return page.isPrevEnabled()
        else: 
            return (page is not self.GetFirstPage())

    def isNextEnabled(self, page):
        if hasattr(page, 'isDynamic') and page.isDynamic():
            return page.isNextEnabled()
        else: return True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class wizard(wxPostCreateWidgetMixin, dialog):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    elementGlobals = dialog.elementGlobals.copy()
    elementGlobals.update(vars(wx.wizard))

    _ctxHostObjNames = ('frame', 'dialog', 'wizard')

    defaultSettings = dialog.defaultSettings.copy()
    defaultSettings.update({ 
        })

    defaultStyleSettings = dialog.defaultStyleSettings.copy()
    defaultStyleSettings.update({
        'style': 'DEFAULT_DIALOG_STYLE | CLIP_CHILDREN',
        'title': 'Wizard',
        'sequential': 'True',
        'autosize': 'True',
        #'size-page': 'None',
        })

    wizardBitmap = None
    wizardPageTypes = wxClasses(wx.wizard.WizardPage, wx.wizard.WizardPageSimple, wx.wizard.PyWizardPage)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Definitions 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def objShow(self, obj, show=True):
        obj.RunWizard()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    if wxVersion() < '2.5':
        # wx-2.4 Wizard process
        def createFrame(self, parentObj):
            kwWX = self.getStyleSettingsCollectionWX(('pos'), localized=('title',))
            obj = SkinWizard(parentObj, **kwWX)
            self.sequential = self.getStyleSettingEval('sequential')
            self.lastPage = None
            return obj
    else:
        # wx-2.5 Wizard process
        def createFrame(self, parentObj):
            kwWX = self.getStyleSettingsCollectionWX(('style', 'pos'), localized=('title',))
            if self.wizardBitmap is not None:
                kwWX['bitmap'] = self.wizardBitmap
            obj = SkinWizard(parentObj, **kwWX)

            sizePage = self.getStyleSettingEval('size-page', None)
            if sizePage: 
                obj.SetPageSize(sizePage)

            self.sequential = self.getStyleSettingEval('sequential')
            self.lastPage = None
            return obj

    def finishFrame(self, obj, parentObj):
        del self.lastPage
        return dialog.finishFrame(self, obj, parentObj)

    if wxVersion() < '2.5':
        def installDefaultEvent(self, evtHandler, evtObject, evtCallback):
            import warnings
            warnings.warn('wxPython version 2.4 does not properly call EVT_WIZARD_FINISHED')
            return wx.wizard.EVT_WIZARD_FINISHED(evtHandler, evtObject.GetId(), evtCallback)
    else:
        def installDefaultEvent(self, evtHandler, evtObject, evtCallback):
            return wx.wizard.EVT_WIZARD_FINISHED(evtHandler, evtObject.GetId(), evtCallback)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def isChildCollector(self):
        return True
    def addCollectedChild(self, childElem, childObj): 
        if isinstance(childObj, self.wizardPageTypes):
            self.addWizardPage(childObj)
            return False

        return dialog.addCollectedChild(self, childElem, childObj) 

    _autoPageSize = None
    def addWizardPage(self, wizardPage, bAdjustTopology=True):
        obj = self.getObject()
        if obj.GetFirstPage() is None:
            obj.SetFirstPage(wizardPage)

        if self.getStyleSettingEval('autosize'):
            sizer = wizardPage.GetSizer()
            if sizer is not None:
                minSize = sizer.CalcMin()
                self._autoPageSize = map(max, zip(minSize, self._autoPageSize or obj.GetPageSize()))
                obj.SetPageSize(self._autoPageSize)

        if bAdjustTopology and self.sequential:
            self.setupSequential(self.lastPage, wizardPage)
            self.lastPage = wizardPage

    def setupSequential(self, prevPage, nextPage):
        if prevPage is None: 
            return
        if nextPage is None: 
            return
        if (prevPage.GetNext() is None) and (nextPage.GetPrev() is None):
            prevPage.SetNext(nextPage)
            nextPage.SetPrev(prevPage)

    def addCollectedBitmapChild(self, childElem, bitmap, purposes):
        for purpose in purposes[:]:
            if purpose in ('', 'default', 'wizard'): 
                self.setWizardBitmap(bitmap)
                purposes.remove(purpose)
        return dialog.addCollectedBitmapChild(self, childElem, bitmap, purposes)

    def setWizardBitmap(self, wizardBitmap):
        self.wizardBitmap = wizardBitmap
        obj = self.getObject()
        assert obj is not None

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    __recursiveLockGetObject = False
    def getObject(self):
        obj = dialog.getObject(self)
        if obj is None and not self.__recursiveLockGetObject:
            # make sure we don't get in here again
            self.__recursiveLockGetObject = True
            try:
                # force the creation of the 
                self.getParentObj()

                # lazy create
                obj = self._tmAssureCreated()
            finally:
                del self.__recursiveLockGetObject
        return obj
        
