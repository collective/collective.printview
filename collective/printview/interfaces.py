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
        title=_(u"Content types to pick for single view"),
        required=False,
        default=['Document'],
        value_type=schema.Choice(
            vocabulary='plone.app.vocabularies.ReallyUserFriendlyTypes')
        )
