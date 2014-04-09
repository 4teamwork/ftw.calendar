from ftw.builder.testing import BUILDER_LAYER
from ftw.builder.testing import functional_session_factory
from ftw.builder.testing import set_builder_session_factory
from ftw.testing import FunctionalSplinterTesting
from plone.app.event.interfaces import IEventSettings
from plone.app.testing import applyProfile
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.registry.interfaces import IRegistry
from plone.testing import z2
from zope.component import getUtility
from zope.configuration import xmlconfig
import ftw.calendar.tests.builders
import os


def os_zone():
    return 'TZ' in os.environ.keys() and os.environ['TZ'] or None


def set_timezone(tz):
    # Set the portal timezone
    reg = getUtility(IRegistry)
    settings = reg.forInterface(IEventSettings, prefix="plone.app.event")
    settings.portal_timezone = tz


class FtwCalendarLayer(PloneSandboxLayer):
    """I would prefere to inherit from PAEventLayer, but this is not possible
    since, it uses robotframework testing and we don't.
    """

    defaultBases = (PLONE_FIXTURE, BUILDER_LAYER)

    def setUpZope(self, app, configurationContext):
        self.ostz = os_zone()

        xmlconfig.string(
            '<configure xmlns="http://namespaces.zope.org/zope">'
            '  <include package="z3c.autoinclude" file="meta.zcml" />'
            '  <includePlugins package="plone" />'
            '  <includePluginsOverrides package="plone" />'
            '</configure>',
            context=configurationContext)

        import ftw.calendar
        xmlconfig.file('configure.zcml', ftw.calendar,
                       context=configurationContext)

        z2.installProduct(app, 'Products.DateRecurringIndex')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'ftw.calendar:paevent')
        applyProfile(portal, 'plone.app.event:testing')
        set_timezone(tz='UTC')

    def tearDownZope(self, app):
        z2.uninstallProduct(app, 'Products.DateRecurringIndex')

        # reset OS TZ
        if self.ostz:
            os.environ['TZ'] = self.ostz
        elif 'TZ' in os.environ:
            del os.environ['TZ']


FTW_CALENDAR_FIXTURE = FtwCalendarLayer()
FTW_CALENDAR_INTEGRATION_TESTING = IntegrationTesting(
    bases=(FTW_CALENDAR_FIXTURE, ), name="FtwCalendar:Integration")
FTW_CALENDAR_FUNCTIONAL_TESTING = FunctionalSplinterTesting(
    bases=(FTW_CALENDAR_FIXTURE,
           set_builder_session_factory(functional_session_factory)),
    name="FtwCalendar:Functional")
