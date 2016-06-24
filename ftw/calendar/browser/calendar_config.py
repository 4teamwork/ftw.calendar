from zope.component.hooks import getSite

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName


class CalendarConfigView(BrowserView):
    """
    Calendar configuration view.
    """

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
