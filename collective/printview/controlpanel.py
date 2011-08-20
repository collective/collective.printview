# -*- coding: utf-8 -*-

from plone.app.registry.browser import controlpanel
from collective.printview.interfaces import IPrintviewSettings
from collective.printview import _


class PrintviewSettingsEditForm(controlpanel.RegistryEditForm):

    schema = IPrintviewSettings
    label = _(u"Printview settings")
    description = _(u"")

    def updateFields(self):
        super(PrintviewSettingsEditForm, self).updateFields()

    def updateWidges(self):
        super(PrintviewSettingsEditForm, self).updateWidgets()


class PrintviewControlPanel(controlpanel.ControlPanelFormWrapper):
    form = PrintviewSettingsEditForm
