# -*- coding: utf-8 -*-

import unittest2 as unittest
from collective.printview.tests.base import MYPRODUCT_INTEGRATION_TESTING
from collective.printview.interfaces import IPrintviewSettings
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_ID
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import setRoles
from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter
from plone.registry import Registry


class IntegrationTest(unittest.TestCase):
    layer = MYPRODUCT_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.workflowTool = getToolByName(self.portal, 'portal_workflow')
        self.workflowTool.setDefaultChain('simple_publication_workflow')

        # login
        login(self.portal, TEST_USER_NAME)
        setRoles(self.portal, TEST_USER_ID, ['Manager','Owner'])

        self.registry = Registry()
        self.registry.registerInterface(IPrintviewSettings)

        # create content folder
        self.portal.invokeFactory('Folder', 'folder', title=u"Folder")
        self.folder = self.portal['folder']

        # create testcontents inside the test folder
        self.folder.invokeFactory('Folder', 'a1', title=u"A1")
        self.folder.invokeFactory('Folder', 'b1', title=u"B1")

        self.subfolder1 = self.folder['a1']
        self.subfolder2 = self.folder['b1']
        self.subfolder1.invokeFactory('Folder', 'a1.1', title=u"A1.1")
        self.subfolder1.invokeFactory('Folder', 'a1.2', title=u"A1.2")

        self.subfolder2.invokeFactory('Folder', 'b1.1', title=u"B1.1")
        self.subfolder2.invokeFactory('Folder', 'b1.2', title=u"B1.2")

        self.folder.invokeFactory('Document', 'root-document', title=u"Root document")
        doc1 = self.folder['root-document']
        doc1.setText("<p>Root foobar</p>")

        self.subfolder1.invokeFactory('Document', 'a1-document', title=u"A1 document")
        doc2 = self.subfolder1['a1-document']
        doc2.setText("<p>A1 foobar</p>")

        self.subfolder2.invokeFactory('Document', 'b1-document', title=u"B1 document")
        doc3 = self.subfolder2['b1-document']
        doc3.setText("<p>B1 foobar</p>")

        self.subsubfolder1 = self.subfolder1['a1.1']
        self.subsubfolder1.invokeFactory('Document', 'a11-document', title=u"A11 document")
        doc4 = self.subsubfolder1['a11-document']
        doc4.setText("<p>A11 foobar</p>")

#        self.subsubfolder2.invokeFactory('Document', 'a12-document', title=u"A12 document")
#        doc5.setText("<p>A12 foobar</p>")
#
#        self.subsubfolder3.invokeFactory('Document', 'b11-document', title=u"B11 document")
#        doc6.setText("<p>B11 foobar</p>")
#
#        self.subsubfolder4.invokeFactory('Document', 'b12-document', title=u"B12 document")
#        doc7.setText("<p>B12 foobar</p>")

    def test_printview(self):
        view = getMultiAdapter((self.folder, self.portal.REQUEST),
                               name="printview")
        self.failUnless(view())

    def test_printview_protected(self):
        from AccessControl import Unauthorized
        logout()
        self.assertRaises(Unauthorized,
                          self.portal.restrictedTraverse,
                         '@@printview')

    def test_printview_owner(self):
        self.failUnless(self.portal.restrictedTraverse('@@printview')())

    def test_controlpanel_view(self):
        view = getMultiAdapter((self.portal, self.portal.REQUEST),
                               name="printview-settings")
        view = view.__of__(self.portal)
        self.failUnless(view())

    def test_controlpanel_view_protected(self):
        from AccessControl import Unauthorized
        logout()
        self.assertRaises(Unauthorized,
                          self.portal.restrictedTraverse,
                         '@@printview-settings')

    def test_record_allowed_states(self):
        record_allowed_states_key = self.registry.records[
            'collective.printview.interfaces.IPrintviewSettings.allowed_states']
        self.failUnless('allowed_states' in IPrintviewSettings)
        self.assertEquals(record_allowed_states_key.value, ['published'])

    def test_record_folderish_types(self):
        record_folderish_types = self.registry.records[
            'collective.printview.interfaces.IPrintviewSettings.folderish_types']
        self.failUnless('folderish_types' in IPrintviewSettings)
        self.assertEquals(record_folderish_types.value, ['Folder'])

    def test_record_types(self):
        record_types = self.registry.records[
            'collective.printview.interfaces.IPrintviewSettings.types']
        self.failUnless('types' in IPrintviewSettings)
        self.assertEquals(record_types.value, ['Document'])

    def test_private_objects_view(self):
        view = self.portal.restrictedTraverse('@@printview')
        view.update()
        view.settings.allowed_states = ['published','private']
        self.failUnless('A1 foobar' in self.portal.restrictedTraverse('@@printview')())

    def test_published_objects_view(self):
        view = self.portal.restrictedTraverse('@@printview')
        self.workflowTool.doActionFor(self.folder, 'publish')
        self.workflowTool.doActionFor(self.folder['root-document'], 'publish')
        self.failUnless('Root foobar' in view())
