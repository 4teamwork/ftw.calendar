from DateTime import DateTime
from datetime import timedelta
from ftw.calendar.browser.interfaces import IFtwCalendarEventCreator
from ftw.calendar.browser.interfaces import IFtwCalendarJSONSourceProvider
from plone import api
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from zope.component import getMultiAdapter
from zope.interface import implements
import simplejson as json


class CalendarJSONSource(object):
    implements(IFtwCalendarJSONSourceProvider)

    def __init__(self, context, request):
        self.context = context
        self.request = request

        self.memberid = \
            self.context.portal_membership.getAuthenticatedMember().id

    def generate_json_calendar_source(self):
        result = []

        for brain in self.get_event_brains():
            result.append(self.generate_source_dict_from_brain(brain))

        return json.dumps(result, sort_keys=True)

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
                args['portal_type'] = portal_calendar.getCalendarTypes()

            return catalog(
                path={'depth': -1,
                      'query': '/'.join(self.context.getPhysicalPath())},
                **args
            )

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

        event = brain.getObject()
        editable = api.user.has_permission('Edit', obj=event)

        # The default source marks an event as all day if it is longer than
        # one day. Marking an event as all day in ftw.contentpage will set
        # the times to 00:00 and 23:59. If those times are on the same
        # date they will not be recognised as all day because thats only a
        # 0.999.. day. This check will mark those events as all day.
        duration = brain.end - brain.start
        if isinstance(duration, timedelta):
            duration = duration.seconds / 60. / 60.
        allday = duration > 0.99

        return {"id": "UID_%s" % (brain.UID),
                "title": title,
                "start": start,
                "end": end,
                "url": brain.getURL(),
                "editable": editable,
                "allDay": allday,
                "className": "state-" + str(brain.review_state)
                + (editable and " editable" or ""),
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


class CalendarAddView(BrowserView):
    def __call__(self):
        request = self.context.REQUEST
        title = request.get('title')
        start_date = DateTime(int(request.get('startdate')))

        if not title or not start_date:
            raise ValueError()

        eventCreator = getMultiAdapter((self.context, request),
                                       IFtwCalendarEventCreator)
        event = eventCreator.createEvent(title, start_date)

        self.request.RESPONSE.redirect(event.absolute_url() + '/edit')
