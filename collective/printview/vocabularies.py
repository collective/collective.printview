# -*- coding: utf-8 -*-

from five import grok
from plone.app.vocabularies.types import BAD_TYPES
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from zope.site.hooks import getSite

from Products.CMFCore.utils import getToolByName


class ReallyUserFriendlyFolderishTypesVocabulary(object):
    """
    Vocabulary factory for really user friendly folderish portal types.
    Vocabulary is based on ReallyUserFriendlyTypesVocabulary from
    plone.app.content.types.
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        site = getSite()
        pc = getToolByName(site, 'portal_catalog', None)
        types = pc.searchResults(object_provides=[
            'plone.dexterity.interfaces.IDexterityContainer',
            'Products.ATContentTypes.interfaces.folder.IATFolder'])
        # We could also use pc.searchResults(is_folderish=True) to
        # get more results (eg. Collections).
        results=list(set([(brain.Type, brain.portal_type) for brain in types]))
        if pc is None:
            return SimpleVocabulary([])

        items = [ptype for ptype in results
                 if ptype[0] not in BAD_TYPES]
        items.sort()
        items = [SimpleTerm(i[1], i[1], i[0]) for i in items]
        return SimpleVocabulary(items)

ReallyUserFriendlyFolderishTypesVocabularyFactory = \
    ReallyUserFriendlyFolderishTypesVocabulary()

grok.global_utility(ReallyUserFriendlyFolderishTypesVocabulary,
    name=u"collective.printview.ReallyUserFriendlyFolderishTypes")
