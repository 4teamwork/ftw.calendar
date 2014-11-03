from ftw.builder.testing import BUILDER_LAYER
from ftw.builder.testing import functional_session_factory
from ftw.builder.testing import set_builder_session_factory
from ftw.testing import FunctionalSplinterTesting
from plone.app.testing import applyProfile
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from zope.configuration import xmlconfig
import ftw.calendar.tests.builders


class FtwCalendarLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, BUILDER_LAYER)

    def setUpZope(self, app, configurationContext):
        import ftw.calendar
        xmlconfig.file('configure.zcml', ftw.calendar,
                       context=configurationContext)

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        applyProfile(portal, 'ftw.calendar:default')


FTW_CALENDAR_FIXTURE = FtwCalendarLayer()
FTW_CALENDAR_INTEGRATION_TESTING = IntegrationTesting(
    bases=(FTW_CALENDAR_FIXTURE, ), name="FtwCalendar:Integration")
FTW_CALENDAR_FUNCTIONAL_TESTING = FunctionalSplinterTesting(
    bases=(FTW_CALENDAR_FIXTURE,
           set_builder_session_factory(functional_session_factory)),
    name="FtwCalendar:Functional")
