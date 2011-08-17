# -*- coding: utf-8 -*-

from zope.interface import implements
from zope.component import adapts
from zope.app.component.hooks import getSite

from plone.fieldsets.fieldsets import FormFields
from plone.app.controlpanel.form import ControlPanelForm

from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.utils import safe_hasattr
from Products.CMFCore.utils import getToolByName
from Products.CMFDefault.formlib.schema import ProxyFieldProperty

from collective.printview.interfaces import IPrintViewControlPanelForm
from collective.printview.interfaces import IPrintViewControlPanel
from collective.printview import _


class PrintViewControlPanelAdapter(SchemaAdapterBase):

    adapts(IPloneSiteRoot)
    implements(IPrintViewControlPanelForm)

    def __init__(self, context):
        super(PrintViewControlPanelAdapter, self).__init__(context)
        self.portal = getSite()
        pprop = getToolByName(self.portal, 'portal_properties')
        self.context = pprop.printview_properties

    allowedStates = ProxyFieldProperty(IPrintViewControlPanelForm['allowedStates'])
    folderishTypes = ProxyFieldProperty(IPrintViewControlPanelForm['folderishTypes'])

    def getAllowedStates(self):
        return getattr(self.context, 'allowedStates',
                       getattr(self.context, 'allowedStates', None))

    def setAllowedStates(self, value):
        if safe_hasattr(self.context, 'allowedStates'):
            self.context.allowedStates = value

    def getFolderishTypes(self):
        return getattr(self.context, 'folderishTypes',
                       getattr(self.context, 'folderishTypes', None))

    def setFolderishTypes(self, value):
        if safe_hasattr(self.context, 'folderishTypes'):
            self.context.folderishTypes = value

    ProxyFieldProperty(IPrintViewControlPanelForm['allowedStates'])
    ProxyFieldProperty(IPrintViewControlPanelForm['folderishTypes'])

class PrintViewControlPanel(ControlPanelForm):
    """ Pathkey control panel """

    implements(IPrintViewControlPanel)

    form_fields = FormFields(IPrintViewControlPanelForm)

    form_name = _(u"PrintView settings")
    label = _(u"PrintView settings")
    description = _(u"Here you can customize PrintView settings")
