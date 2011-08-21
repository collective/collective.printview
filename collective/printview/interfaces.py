# -*- coding: utf-8 -*-

from plone.theme.interfaces import IDefaultPloneLayer
from zope.interface import Interface
from zope import schema
from collective.printview import _


class IPrintviewBrowserLayer(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 skin layer bound to a skin
    selection in portal_skins.
    """


class IPrintviewSettings(Interface):

    allowed_states = schema.List(
        title=_(u"Queried workflow states"),
        description=_(u"Select the workflow states which will be used for \
                      searching both folders to crawl through and content types \
                      to get the actual data for view."),
        required=False,
        default=['published',],
        value_type=schema.Choice(
            vocabulary='plone.app.vocabularies.WorkflowStates',)
        )

    folderish_types = schema.List(
        title=_(u"Folderish content types"),
        description=_(u"Specify all the folderish content types you wan't\
                      to crawl through."),
        required=False,
        default=['Folder'],
        value_type=schema.Choice(
            vocabulary='collective.printview.ReallyUserFriendlyFolderishTypes')
        )

    types = schema.List(
        title=_(u"Content types"),
        description=_(u"Select the content types which you want to use to gather \
                      the data for the printable view."),
        required=False,
        default=['Document'],
        value_type=schema.Choice(
            vocabulary='plone.app.vocabularies.ReallyUserFriendlyTypes')
        )
