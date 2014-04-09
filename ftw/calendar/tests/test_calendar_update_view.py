from DateTime import DateTime
from datetime import datetime
from ftw.builder import Builder
from ftw.builder import create
from ftw.calendar.browser.interfaces import IFtwCalendarLayer
from ftw.calendar.testing import FTW_CALENDAR_FUNCTIONAL_TESTING
from plone.app.event.dx.behaviors import IEventRecurrence
from plone.app.event.interfaces import IBrowserLayer
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.uuid.interfaces import IUUID
from unittest2 import TestCase
from zope.interface import alsoProvides
import json


TZNAME = "Europe/Vienna"


class TestCalendarUpdateView(TestCase):

    layer = FTW_CALENDAR_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        alsoProvides(self.portal.REQUEST, IFtwCalendarLayer)
        alsoProvides(self.portal.REQUEST, IBrowserLayer)

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

    def test_result_using_dx_event(self):
        folder = create(Builder('folder'))
        event = folder.get(
            folder.invokeFactory(
                'plone.app.event.dx.event',
                'event1',
                title=u'Event',
                description=u'Description',
                start=datetime(2000, 01, 01, 12, 0),
                end=datetime(2000, 01, 01, 14, 0),
                timezone=TZNAME,
                whole_day=False
            ))

        expect = {u'id': u'UID_{0}'.format(IUUID(event)),
                  u'title': u'Event',
                  u'start': DateTime(
                      '2000/01/01 12:00:00 %s' % TZNAME).ISO8601(),
                  u'end': DateTime(
                      '2000/01/01 14:00:00 %s' % TZNAME).ISO8601(),
                  u'url': event.absolute_url().decode('utf-8'),
                  u'allDay': False,
                  u'editable': True,
                  u'className': u'state- editable',
                  u'description': u'Description'}

        self.assertEquals(
            expect,
            json.loads(folder.restrictedTraverse('@@ftwcalendar_update')())[0])

    def test_result_using_dx_event_with_recurrence(self):
        folder = create(Builder('folder'))
        event = folder.get(
            folder.invokeFactory(
                'plone.app.event.dx.event',
                'event1',
                title=u'Event',
                description=u'Description',
                start=datetime(2000, 01, 01, 12, 0),
                end=datetime(2000, 01, 01, 14, 0),
                timezone=TZNAME,
                whole_day=False
            ))
        event_w_rec = IEventRecurrence(event)
        event_w_rec.recurrence = 'RRULE:FREQ=DAILY;COUNT=4'
        event.reindexObject()

        result = json.loads(
            folder.restrictedTraverse('@@ftwcalendar_update')())

        self.assertEquals(
            4, len(result), 'Expect 4 items')

        expect_event = {u'id': u'UID_{0}'.format(IUUID(event)),
                        u'title': u'Event',
                        u'start': DateTime(
                            '2000/01/01 12:00:00 %s' % TZNAME).ISO8601(),
                        u'end': DateTime(
                            '2000/01/01 14:00:00 %s' % TZNAME).ISO8601(),
                        u'url': event.absolute_url().decode('utf-8'),
                        u'allDay': False,
                        u'editable': True,
                        u'className': u'state- editable',
                        u'description': u'Description'}

        self.assertEquals(expect_event, result[0])

        expect_last_occ = {u'allDay': False,
                           u'className': u'',
                           u'description': 'Description',
                           u'editable': False,
                           u'end': u'2000-01-04T14:00:00+01:00',
                           u'id': u'UID_{0}'.format(IUUID(event)),
                           u'start': u'2000-01-04T12:00:00+01:00',
                           u'title': u'Event',
                           u'url': u'http://nohost/plone/folder/event1/2000-01-04'}

        self.assertEquals(expect_last_occ, result[-1])
