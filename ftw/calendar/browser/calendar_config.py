from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

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

        calendar_tool = getToolByName(self.context, 'portal_calendar')
        first = calendar_tool.getFirstWeekDay()
        return (first < 6 and first + 1) or 0
