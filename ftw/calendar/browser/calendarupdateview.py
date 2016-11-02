from DateTime import DateTime
from ftw.calendar.browser.interfaces import IEventCssKlassGenerator
from ftw.calendar.browser.interfaces import IFtwCalendarJSONSourceProvider
from plone.app.event.base import dates_for_display
from plone.app.event.base import get_events
from plone.app.event.base import RET_MODE_ACCESSORS
from plone.app.event.base import RET_MODE_BRAINS
from plone.memoize import ram
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.ZCatalog.interfaces import ICatalogBrain
from zope.component import adapts
from zope.component import getMultiAdapter
from zope.component import queryMultiAdapter
from zope.interface import implements
from zope.interface import Interface
import json


def _data_with_recurence_cache(method, self, range_):
    query = {}
    query['path'] = {'depth': -1,
                     'query': '/'.join(self.context.getPhysicalPath())}

    brains = get_events(self.context,
                        start=range_['start'],
                        end=range_['end'],
                        expand=True,
                        ret_mode=RET_MODE_BRAINS,
                        **query)
    return tuple([brain.modified for brain in brains]) + (range_['start'],
                                                          range_['end'])


class CalendarJSONSource(object):
    implements(IFtwCalendarJSONSourceProvider)

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.cache = []

        self.memberid = \
            self.context.portal_membership.getAuthenticatedMember().id

    def generate_json_calendar_source(self):
        self.cache = []

        return json.dumps(self.get_event_data(), sort_keys=True)

    def get_event_data(self):
        result = []
        # Range defined by fullcalender
        range_ = {
            'start': {
                'query': DateTime(self.request.get('end')), 'range': 'max'},
            'end': {
                'query': DateTime(self.request.get('start')), 'range': 'min'}}

        result += self.get_data_with_recurrence(range_)
        result += self.get_data_without_recurrence(range_)

        return result

    def get_data_without_recurrence(self, range_):
        result = []

        if self.context.portal_type in ['Topic', 'Collection']:
            brains = self.context.aq_inner.queryCatalog(
                REQUEST=self.request, **range_)
        else:
            portal_calendar = getToolByName(self.context, 'portal_calendar')
            catalog = getToolByName(self.context, 'portal_catalog')
            brains = catalog(
                portal_type=portal_calendar.getCalendarTypes(),
                path={'depth': -1,
                      'query': '/'.join(self.context.getPhysicalPath())}
            )

        for brain in brains:
            url = brain.getURL()
            if url not in self.cache:
                self.cache.append(url)
                result.append(self.format_brain(brain))
        return result

    def format_brain(self, brain):
        editable = self.memberid in brain.Creator
        # XXX This is no a good solution, the user should decide if it is
        # a all day event or not unfortunately the old ATEvent does not support
        # this field - therefore we just say if it's equal or longer than one
        # day it's displayed as all day event.
        allday = brain.end - brain.start >= 1.0
        css = queryMultiAdapter(
            (brain, self.request),
            name="event_css_klass_generator").generate_css_klasses()

        return {"id": "UID_%s" % (brain.UID),
                "title": brain.Title,
                "start": brain.start.ISO8601(),
                "end": brain.end.ISO8601(),
                "url": brain.getURL(),
                "editable": editable,
                "allDay": allday,
                "className": css + (editable and " editable" or ""),
                "description": brain.Description}

    @ram.cache(_data_with_recurence_cache)
    def get_data_with_recurrence(self, range_):
        result = []
        query = {}
        query['path'] = {'depth': -1,
                         'query': '/'.join(self.context.getPhysicalPath())}

        occurencies = get_events(self.context,
                                 start=range_['start'],
                                 end=range_['end'],
                                 expand=True,
                                 ret_mode=RET_MODE_ACCESSORS,
                                 **query)

        for occ in occurencies:
            url = occ.url
            if url not in self.cache:
                self.cache.append(url)
                result.append(self.format_occurency(occ))
        return result

    def format_occurency(self, occ):
        dates = dates_for_display(occ)
        css = queryMultiAdapter(
            (occ, self.request),
            name="event_css_klass_generator").generate_css_klasses()

        return {"id": "UID_%s" % (occ.uid),
                "title": occ.title,
                "start": dates['start_iso'],
                "end": dates['end_iso'],
                "url": occ.url,
                "editable": False,
                "allDay": dates['whole_day'],
                "className": css,
                "description": occ.description}


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


class DefaultEventCssKlassGenerator(object):
    implements(IEventCssKlassGenerator)
    adapts(Interface, Interface)

    def __init__(self, item, request):
        self.item = item
        self.request = request

    def generate_css_klasses(self):
        return ""


class BrainEventCssKlassGenerator(object):
    implements(IEventCssKlassGenerator)
    adapts(ICatalogBrain, Interface)

    def __init__(self, item, request):
        self.item = item
        self.request = request

    def generate_css_klasses(self):
        return "state-" + str(self.item.review_state)


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
