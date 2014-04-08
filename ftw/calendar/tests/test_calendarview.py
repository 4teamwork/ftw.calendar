from ftw.calendar.browser.interfaces import IFtwCalendarLayer
from ftw.calendar.testing import FTW_CALENDAR_FUNCTIONAL_TESTING
from ftw.testbrowser import browsing
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from Products.CMFCore.utils import getToolByName
from unittest2 import TestCase
from zope.interface import directlyProvides


class TestCalendarView(TestCase):

    layer = FTW_CALENDAR_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)

    def test_if_p_a_event_is_installed(self):
        portal_setup = getToolByName(self.portal, 'portal_setup')

        version = portal_setup.getLastVersionForProfile(
            'plone.app.event:default')
        self.assertNotEqual(version, None)
        self.assertNotEqual(version, 'unknown')

    def test_calendarview_available(self):
        directlyProvides(self.portal.REQUEST, IFtwCalendarLayer)
        view = self.portal.restrictedTraverse('@@ftwcalendar_view')

        self.assertTrue(view, 'ftw calendar view is not available')

    @browsing
    def test_calendar_view(self, browser):
        browser.visit(self.portal, view='ftwcalendar_view')

        element = browser.css('#calendar')
        self.assertTrue(element, 'Not div with if "calendar" found')
