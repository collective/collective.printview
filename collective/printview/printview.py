# -*- coding: utf-8 -*-

from Acquisition import aq_inner
from zope.component import getUtility
from five import grok
from plone.registry.interfaces import IRegistry
from collective.printview.interfaces import IPrintviewSettings
from Products.CMFCore.utils import getToolByName
from plone.memoize import ram
from Products.CMFCore.interfaces import IFolderish


def _modified_cachekey(method, self):
    """ Returns DateTime of the latest modification """
    catalog = getToolByName(self, 'portal_catalog')
    portal_types = self.settings.folderish_types + \
                   self.settings.types
    latest = catalog(portal_types=portal_types,
                     path={'query':'/'.join(self.context.getPhysicalPath())},
                     review_state=self.settings.allowed_states,
                     sort_on='modified',
                     sort_order='ascending')

    if latest:
        hash_string = self.settings.allowed_states.__str__() + \
            self.settings.folderish_types.__str__() + \
            self.settings.types.__str__() + \
            latest[-1].modified.ISO()
        return hash(hash_string)
    else:
        pass


class Printview(grok.View):
    """ Support class for printview view """

    grok.name('printview')
    grok.context(IFolderish)
    grok.require('cmf.ManagePortal')

    def update(self):
        registry = getUtility(IRegistry)
        self.settings = registry.forInterface(IPrintviewSettings)
        self.pages_data = []

    @ram.cache(_modified_cachekey)
    def getAllPages(self):
        """Call getPages method to start crawling."""

        context = aq_inner(self.context)
        self.getPages(context)

        return self.pages_data

    def getPages(self, obj):
        """
        Crawls through folders and documents and adds all public or visible
        documents to a list for printing.
        """

        for content in obj.getFolderContents(contentFilter = {
            'portal_type': self.settings.types,
            'review_state': self.settings.allowed_states},
            full_objects=True):
            try:
                self.pages_data.append({
                    "title": content.Title(),
                    "description": content.Description(),
                    "data": content.getText()
                    })
            except AttributeError:
                # Maybe we have dexterity content type with RichText data
                # TODO: fix stupid repeat
                self.pages_data.append({
                    "title": content.Title(),
                    "description": content.Description(),
                    "data": content.text.raw
                    })

        # Get all folderish types in context
        for container in obj.getFolderContents(contentFilter={
            'portal_type': self.settings.folderish_types,
            'review_state': self.settings.allowed_states},
            full_objects=True):

            self.getPages(container)
