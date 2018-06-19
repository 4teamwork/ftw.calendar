from ftw.calendar.browser.interfaces import IFtwCalendarEventCreator
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from zope.component import ComponentLookupError
from zope.component import getMultiAdapter
from zope.component.hooks import getSite


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
        calendar_tool = getToolByName(self.context, 'portal_calendar', None)
        if calendar_tool:
            first = calendar_tool.getFirstWeekDay()
        else:
            first = getSite().portal_registry['plone.first_weekday']
        return (first < 6 and first + 1) or 0

    def can_add_content(self):
        try:
            eventCreator = getMultiAdapter((self.context, self.request),
                                           IFtwCalendarEventCreator)
        except ComponentLookupError:
            return False

        return eventCreator.getEventType() in \
               self.context.getImmediatelyAddableTypes()
