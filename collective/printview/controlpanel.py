# -*- coding: utf-8 -*-

from plone.app.registry.browser import controlpanel
from collective.printview.interfaces import IPrintviewSettings
from collective.printview import _


class PrintviewSettingsEditForm(controlpanel.RegistryEditForm):

    schema = IPrintviewSettings
    label = _(u"Printview settings")
    description = _(u"Here you can configure which workflow states and content\
                      types are included in printview view. Please note, that\
                      if you're using printview with a site with lots of content \
                      objects it may slow the site for other users.")

    def updateFields(self):
        super(PrintviewSettingsEditForm, self).updateFields()

    def updateWidges(self):
        super(PrintviewSettingsEditForm, self).updateWidgets()


class PrintviewControlPanel(controlpanel.ControlPanelFormWrapper):
    form = PrintviewSettingsEditForm
