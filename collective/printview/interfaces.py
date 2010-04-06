from plone.theme.interfaces import IDefaultPloneLayer
from zope.interface import Interface

class IPrintViewBrowserLayer(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 skin layer bound to a skin
    selection in portal_skins.
    """

class IPrintView(Interface):
    """ 
    Browser view for displaying every documents body from all the folders
    under the path this view is called from.
    """
    
    def getAllPages():
        """
        Checks if we're allowed to crawl through folder contents from
        folders print_contents property. If boolean is true, we'll call
        getPages method to start crawling - if property is false, we'll 
        add error message to our list and return it. 
        """
        
        pass
    
    def getPages():
        """
        Crawls through folders and documents and adds all public or visible
        documents to a list for printing.
        """
        
        pass
    