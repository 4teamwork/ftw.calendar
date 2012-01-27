from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from DateTime import DateTime

#from ftw.calendar import calendarMessageFactory as _
import simplejson as json


class CalendarupdateView(BrowserView):
    """
    Calendarupdate browser view
    """


    def __call__(self, *args, **kw):
        """Render JS Initialization code"""

        response = self.request.response
        context = self.context

        response.setHeader('Content-Type', 'application/x-javascript')

        args = {
            'start': {
                'query': DateTime(self.request.get('end')), 'range': 'max'},
            'end': {
                'query': DateTime(self.request.get('start')), 'range': 'min'}}
        if context.portal_type == 'Topic':
            brains = context.aq_inner.queryCatalog(REQUEST=self.request, **args)
        else:
            portal_calendar = getToolByName(context, 'portal_calendar')
            catalog = getToolByName(context, 'portal_catalog')
            brains = catalog(
                portal_type = portal_calendar.getCalendarTypes(),
                path = {'depth': -1,
                        'query': '/'.join(context.getPhysicalPath())}
            )
        result = []
        memberid = self.context.portal_membership.getAuthenticatedMember().id

        for brain in brains:
            if memberid in brain.Creator:
                editable = True
            else:
                editable = False
            if brain.end - brain.start > 1.0:
                allday = True
            else:
                allday = False
            result.append({"id": "UID_%s" % (brain.UID),
                           "title": brain.Title,
                           "start": brain.start.rfc822(),
                           "end": brain.end.rfc822(),
                           "url": brain.getURL(),
                           "editable": editable,
                           "allDay": allday,
                           "className": "state-" + str(brain.review_state) + \
                                (editable and " editable" or ""),
                           "description": brain.Description})
        return json.dumps(result, sort_keys=True)


class CalendarDropView(BrowserView):

    def __call__(self):
        request = self.context.REQUEST

        event_uid = request.get('event')

        if event_uid:
            event_uid = event_uid.split('UID_')[1]
        brains = self.context.portal_catalog(UID = event_uid)

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
        brains = self.context.portal_catalog(UID = event_uid)
        obj = brains[0].getObject()
        endDate = obj.endDate
        dayDelta, minuteDelta = float(request.get('dayDelta')), \
            float(request.get('minuteDelta'))

        endDate = endDate + dayDelta + minuteDelta / 1440.0

        obj.setEndDate(endDate)
        obj.reindexObject()
        return True
