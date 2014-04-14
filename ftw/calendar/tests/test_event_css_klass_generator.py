from ftw.builder import Builder
from ftw.builder import create
from ftw.calendar.testing import FTW_CALENDAR_INTEGRATION_TESTING
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from unittest2 import TestCase
from zope.component import queryMultiAdapter
from zope.interface import Interface


class TestEventCSSKlassGenerators(TestCase):

    layer = FTW_CALENDAR_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)

    def test_default_css_generator(self):
        default = queryMultiAdapter((Interface, Interface),
                                    name="event_css_klass_generator")

        self.assertEquals("",
                          default.generate_css_klasses(),
                          'The default implementation should be empty.')

    def test_brain_css_generator(self):
        create(Builder('at event'))
        brain = self.portal.portal_catalog({})[0]
        default = queryMultiAdapter((brain, Interface),
                                    name="event_css_klass_generator")

        self.assertEquals("state-",
                          default.generate_css_klasses())
