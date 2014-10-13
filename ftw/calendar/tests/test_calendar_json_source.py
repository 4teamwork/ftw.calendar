from ftw.builder import Builder
from ftw.builder import create
from ftw.calendar.browser.calendarupdateview import CalendarJSONSource
from ftw.calendar.browser.interfaces import IFtwCalendarJSONSourceProvider
from ftw.calendar.testing import FTW_CALENDAR_FUNCTIONAL_TESTING
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from unittest2 import TestCase
from zope.component import getMultiAdapter
from zope.interface.verify import verifyObject


class TestCalendarSource(TestCase):

    layer = FTW_CALENDAR_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)

        self.event = create(Builder('event'))

    def test_adapter_provides_methods(self):
        verifyObject(IFtwCalendarJSONSourceProvider, CalendarJSONSource(
            self.portal, self.portal.REQUEST))

    def test_default_json_source_adapter(self):
        adapter = getMultiAdapter((self.portal, self.portal.REQUEST),
                                  name='ftw_calendar_source')

        self.assertEquals(1,
                          len(adapter.get_event_brains()))

        brain = adapter.get_event_brains()[0]

        self.assertEquals(
            ['className', 'start', 'allDay', 'end', 'description',
             'title', 'url', 'editable', 'id'],
            adapter.generate_source_dict_from_brain(brain).keys())
