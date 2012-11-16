# -*- coding: utf-8 -*-
"""Download 'printview' as PDF"""

import re
import urlparse

from StringIO import StringIO
from DateTime import DateTime
from urllib import unquote

from five import grok

from plone.subrequest import subrequest

from Products.CMFCore.interfaces import IFolderish
from Products.CMFCore.utils import getToolByName

from collective.printview.interfaces import IPrintviewBrowserLayer

from xhtml2pdf.document import pisaDocument


class PrintviewPDF(grok.View):

    grok.name('printview-pdf')
    grok.context(IFolderish)
    grok.layer(IPrintviewBrowserLayer)
    grok.require('cmf.ManagePortal')

    def render(self):
        pdf = StringIO()

        def fetch_resources(uri, rel):
            """ Callback to allow pisa/reportlab to retrieve
            Images,Stylesheets, etc.

            `uri` is the href attribute from the html link element.
            `rel` gives a relative path, but it's not used here.

            See also: https://gist.github.com/2973355
            """
            urltool = getToolByName(self.context, 'portal_url')
            portal_url = urltool.getPortalObject().absolute_url()

            if uri.startswith(portal_url):

                response = subrequest(unquote(uri[len(portal_url) + 1:]))
                if response.status != 200:
                    return None
                try:
                    # Stupid pisa doesn't let me send charset.
                    ctype, encoding =\
                        response.getHeader('content-type').split('charset=')
                    ctype = ctype.split(';')[0]

                    # Pisa only likes ascii css
                    data = response.getBody()\
                        .decode(encoding).encode('ascii', 'ignore')
                except ValueError:
                    ctype = response.getHeader('content-type').split(';')[0]
                    data = response.getBody()

                data = data.encode('base64').replace('\n', '')
                data_uri = 'data:{0};base64,{1}'.format(ctype, data)

                # XXX: Pisa does not seem to be able to handle CSS-files as
                # data uris (it crashes), so lets return only images:
                if ctype.startswith('image'):
                    return data_uri

            return uri

        printview = self.context.restrictedTraverse("printview")

        html = printview().encode('utf-8', 'ignore')
        # Hide "Links"-section added by printview:
        html = html.replace('<div id="links">', '<div style="display: none;">')
        # Transform all links to absolute, to make them links in PDF:
        base_url = self.context.absolute_url()
        for url in re.findall(r'href="([^"]*)"', html):
            html = html.replace('href="%s"' % url,
                                'href="%s"' % urlparse.urljoin(base_url, url))
        html = StringIO(html)

        pisaDocument(html, pdf, raise_exception=True,
                     link_callback=fetch_resources, encoding='utf-8')
        assert pdf.len != 0, 'Pisa PDF generation returned empty PDF!'
        html.close()

        pdfcontent = pdf.getvalue()
        pdf.close()

        now = DateTime()
        nice_filename = '%s_%s' % (self.context.getId().capitalize(),
                                   now.strftime('%Y%m%d'))

        self.request.response.setHeader('Content-Disposition',
                                        'attachment; filename=%s.pdf' %
                                        nice_filename)
        self.request.response.setHeader('Content-Type', 'application/pdf')
        self.request.response.setHeader('Content-Length', len(pdfcontent))
        self.request.response.setHeader('Last-Modified',
                                        DateTime.rfc822(DateTime()))
        self.request.response.setHeader('Cache-Control', 'no-store')
        self.request.response.setHeader('Pragma', 'no-cache')
        self.request.response.write(pdfcontent)

        return pdfcontent
