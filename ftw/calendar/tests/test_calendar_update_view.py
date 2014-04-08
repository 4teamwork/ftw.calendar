from DateTime import DateTime
from ftw.builder import Builder
from ftw.builder import create
from ftw.calendar.browser.interfaces import IFtwCalendarLayer
from ftw.calendar.testing import FTW_CALENDAR_FUNCTIONAL_TESTING
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.uuid.interfaces import IUUID
from unittest2 import TestCase
from zope.interface import directlyProvides
import json


class TestCalendarUpdateView(TestCase):

    layer = FTW_CALENDAR_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        directlyProvides(self.portal.REQUEST, IFtwCalendarLayer)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)

    def test_result_using_at_events(self):
        folder = create(Builder('folder'))
        event = create(Builder('at event')
                       .within(folder)
                       .titled('Event')
                       .having(description='Description')
                       .having(start=DateTime('2000/01/01 12:00'))
                       .having(end=DateTime('2000/01/01 14:00')))

        expect = {u'id': u'UID_{0}'.format(IUUID(event)),
                  u'title': u'Event',
                  u'start': event.start().ISO8601().decode('utf-8'),
                  u'end': event.end().ISO8601().decode('utf-8'),
                  u'url': event.absolute_url().decode('utf-8'),
                  u'allDay': False,
                  u'editable': True,
                  u'className': u'state- editable',
                  u'description': u'Description'}

        self.assertEquals(
            expect,
            json.loads(folder.restrictedTraverse('@@ftwcalendar_update')())[0])
