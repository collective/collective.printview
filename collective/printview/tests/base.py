from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import applyProfile


class MyProduct(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import five.grok
        self.loadZCML(name='configure.zcml', package=five.grok)
        import collective.printview
        self.loadZCML(name='configure.zcml', package=collective.printview)
        self.loadZCML(package=collective.printview)

        # Install product and call its initialize() function
        # z2.installProduct(app, '${namespace_package}.${package}')
        # Note: you can skip this if my.product is not a Zope 2-style
        # product, i.e. it is not in the Products.* namespace and it
        # does not have a <five:registerPackage /> directive in its
        # configure.zcml.

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        applyProfile(portal, 'collective.printview:default')

    def tearDownZope(self, app):
        # Uninstall product
        # z2.uninstallProduct(app, '${namespace_package}.${package}')
        # Note: Again, you can skip this if my.product is not a Zope 2-
        # style product
        pass


MYPRODUCT_FIXTURE = MyProduct()
MYPRODUCT_INTEGRATION_TESTING = IntegrationTesting(bases=(MYPRODUCT_FIXTURE,), name="MyProduct:Integration")
