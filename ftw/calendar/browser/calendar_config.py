from ftw.calendar.browser.interfaces import IFtwCalendarEventCreator
from plone import api
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from zope.component import ComponentLookupError
from zope.component import getMultiAdapter


class CalendarConfigView(BrowserView):
    """
    Calendar configuration view.
    """

    def __call__(self):
        self.request.response.setHeader('X-Theme-Disabled', 'True')
        return super(CalendarConfigView, self).__call__()

    def first_day(self):
        """
        Returns the first day of the week as an integer.
        """
        calendar_tool = getToolByName(api.portal.get(), 'portal_calendar')
        first = calendar_tool.getFirstWeekDay()
        return (first < 6 and first + 1) or 0

    def can_add_content(self):
        try:
            eventCreator = getMultiAdapter((self.context, self.request),
                                           IFtwCalendarEventCreator)
        except ComponentLookupError:
            return False

        return eventCreator.getEventType() in \
               self.context.getImmediatelyAddableTypes()
