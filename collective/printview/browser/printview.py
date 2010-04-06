# -*- coding: utf-8 -*-

from collective.printview.interfaces import IPrintView
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.memoize.instance import memoize
from zope.interface import implements
from collective.printview import _

class PrintView(BrowserView):
    """ Support class for printview view """

    implements(IPrintView)
    
    __call__ = ViewPageTemplateFile('printview.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.pages_data = []        


    def getAllPages(self):
        """
        Checks if we're allowed to crawl through folder contents from
        folders print_contents property. If boolean is true, we'll call
        getPages method to start crawling - if property is false, we'll 
        add error message to our list and return it. 
        """

        self.print_contents = getattr(self.context, 'print_contents', False)

        if self.print_contents:
            self.getPages(self.context)
        else:
            import zope.i18n
            translated_message = zope.i18n.translate(
                msgid   = "printview_crawling_forbidden", 
                domain  = "collective.printview",
                default = "Retrieving folder contents is forbidden.",
                target_language = self.context.REQUEST.get("LANGUAGE", "en"))

            self.pages_data.append({
                "title" :       translated_message,
                "description" : "",
                "data" :        ""})

        return self.pages_data

    def getPages(self, obj):
        """
        Crawls through folders and documents and adds all public or visible
        documents to a list for printing.
        """
        
        review_state_options = ('visible', 'published',)

        for i in obj.getFolderContents(contentFilter = {'portal_type' : 'Document', 'review_state' : review_state_options}, full_objects=True):
            self.pages_data.append({
                "title" :       i.Title(),
                "description" : i.Description(),
                "data" :        i.getText()
            })

        #Get all folders in context
        for j in obj.getFolderContents(contentFilter = {'portal_type' : 'Folder', 'review_state' : review_state_options }, full_objects=True):
            print_contents = getattr(j, 'print_contents', False)
            if print_contents:
                self.getPages(j)