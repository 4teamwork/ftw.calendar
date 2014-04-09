from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
import json


class CalendarupdateView(BrowserView):
    """
    Calendarupdate browser view
    """

    def __init__(self, context, request):
        super(CalendarupdateView, self).__init__(context, request)
        self.result = None
        self.cache = None
        self.memberid = None

    def __call__(self, *args, **kw):
        """Render JS Initialization code"""
        mtool = getToolByName(self.context, 'portal_membership')

        self.result = []
        self.cache = set()
        self.memberid = mtool.getAuthenticatedMember().id

        query = {
            'start': {
                'query': DateTime(self.request.get('end')), 'range': 'max'},
            'end': {
                'query': DateTime(self.request.get('start')), 'range': 'min'}}

        self.get_data_without_recurrence(query)

        response = self.request.response
        response.setHeader('Content-Type', 'application/x-javascript')
        return json.dumps(self.result, sort_keys=True)

    def get_data_without_recurrence(self, query):

        if self.context.portal_type == 'Topic':
            brains = self.context.aq_inner.queryCatalog(
                REQUEST=self.request, **query)
        else:
            portal_calendar = getToolByName(self.context, 'portal_calendar')
            catalog = getToolByName(self.context, 'portal_catalog')
            brains = catalog(
                portal_type=portal_calendar.getCalendarTypes(),
                path={'depth': -1,
                      'query': '/'.join(self.context.getPhysicalPath())}
            )

        for brain in brains:
            uid = brain.UID
            if uid not in self.cache:
                self.cache.add(uid)
                self.result.append(self.format_brain(brain))

    def format_brain(self, brain):
        editable = self.memberid in brain.Creator
        allday = brain.end - brain.start > 1.0

        return {"id": "UID_%s" % (brain.UID),
                "title": brain.Title,
                "start": brain.start.ISO8601(),
                "end": brain.end.ISO8601(),
                "url": brain.getURL(),
                "editable": editable,
                "allDay": allday,
                "className": "state-" + str(brain.review_state) +
                (editable and " editable" or ""),
                "description": brain.Description}


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
