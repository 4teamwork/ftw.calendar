import datetime
from DateTime import DateTime
from ftw.calendar.browser.interfaces import IFtwCalendarJSONSourceProvider
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from zope.component import getMultiAdapter
from zope.interface import implements
import simplejson as json
from plone.app.event.base import get_events
from plone.app.event.base import RET_MODE_ACCESSORS
from email.utils import formatdate
from datetime import timedelta
import time


def rfc822_dt(dt):
    return formatdate(time.mktime(dt.timetuple()))


class CalendarJSONSource(object):
    implements(IFtwCalendarJSONSourceProvider)

    def __init__(self, context, request):
        self.context = context
        self.request = request

        self.memberid = \
            self.context.portal_membership.getAuthenticatedMember().id

    def generate_json_calendar_source(self):
        return json.dumps(list(self.all_events()), sort_keys=True)

    def get_event_brains(self):
        args = {
            'start': {
                'query': DateTime(self.request.get('end')), 'range': 'max'},
            'end': {
                'query': DateTime(self.request.get('start')), 'range': 'min'}}
        if self.context.portal_type in ['Topic', 'Collection']:
            return self.context.aq_inner.queryCatalog(args)
        else:
            catalog = getToolByName(self.context, 'portal_catalog')
            portal_calendar = getToolByName(self.context, 'portal_calendar',
                                            None)
            if portal_calendar:
                portal_type = portal_calendar.getCalendarTypes()
            else:
                portal_type = None
            return catalog(
                portal_type=portal_type,
                path={'depth': -1,
                      'query': '/'.join(self.context.getPhysicalPath())}
            )

    def all_events(self):
        events = get_events(self.context,
                            ret_mode=RET_MODE_ACCESSORS,
                            expand=True,
                            start=DateTime(self.request.get('start')),
                            end=DateTime(self.request.get('end')))

        for event in events:
            duration = event.end - event.start
            yield {"id": "UID_%s" % (event.uid),
                   "title": event.title,
                   "location": event.location,
                   "start": rfc822_dt(event.start),
                   "end": rfc822_dt(event.end),
                   "url": event.url,
                   "editable": False,
                   "allDay": (event.whole_day or duration >
                              timedelta(seconds=86390)),
                   "className": '',
                   "description": event.description}

    def generate_source_dict_from_brain(self, brain):
        #  plone 4-5 compat
        creator = brain.Creator
        if callable(creator):
            creator = creator()
        title = brain.Title
        if callable(title):
            title = title()
        description = brain.Description
        if callable(description):
            description = description()
        start = brain.start
        end = brain.end
        iso = hasattr(start, 'isoformat') and 'isoformat' or 'ISO8601'
        start = getattr(start, iso)()
        end = getattr(end, iso)()

        if isinstance(brain.end - brain.start, float):
            delta = 1.0
        else:
            # delta set to slightly (10 seconds) shorter than a full day so
            # whole day events are handled correctly
            delta = datetime.timedelta(seconds=86390)

        if self.memberid in creator:
            editable = True
        else:
            editable = False
        if brain.end - brain.start > delta:
            allday = True
        else:
            allday = False
        return {"id": "UID_%s" % (brain.UID),
                "title": title,
                "start": start,
                "end": end,
                "url": brain.getURL(),
                "editable": editable,
                "allDay": allday,
                "className": "state-" + str(brain.review_state) +
                (editable and " editable" or ""),
                "description": description}


class CalendarupdateView(BrowserView):
    """ Calendarupdate browser view
    """

    def __call__(self, *args, **kw):
        """Render JS Initialization code"""

        response = self.request.response

        source_provider = getMultiAdapter((self.context, self.request),
                                          name='ftw_calendar_source')

        response.setHeader('Content-Type', 'application/json')
        return source_provider.generate_json_calendar_source()


class CalendarDropView(BrowserView):

    def __call__(self):
        request = self.context.REQUEST

        event_uid = request.get('event')

        if event_uid:
            event_uid = event_uid.split('UID_')[1]
        brains = self.context.portal_catalog(UID=event_uid)

        obj = brains[0].getObject()
        startDate, endDate = obj.startDate, obj.endDate
        dayDelta, minuteDelta = float(request.get('dayDelta')), \
            float(request.get('minuteDelta'))

        startDate = startDate + dayDelta + minuteDelta / 1440.0
        endDate = endDate + dayDelta + minuteDelta / 1440.0

        obj.setStartDate(startDate)
        obj.setEndDate(endDate)
        obj.reindexObject()
        return True


class CalendarResizeView(BrowserView):

    def __call__(self):
        request = self.context.REQUEST
        event_uid = request.get('event')
        if event_uid:
            event_uid = event_uid.split('UID_')[1]
        brains = self.context.portal_catalog(UID=event_uid)
        obj = brains[0].getObject()
        endDate = obj.endDate
        dayDelta, minuteDelta = float(request.get('dayDelta')), \
            float(request.get('minuteDelta'))

        endDate = endDate + dayDelta + minuteDelta / 1440.0

        obj.setEndDate(endDate)
        obj.reindexObject()
        return True
