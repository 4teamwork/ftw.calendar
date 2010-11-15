from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

#from ftw.calendar import calendarMessageFactory as _


class ICalendarView(Interface):
    """
    Calendar View interface
    """


class CalendarView(BrowserView):
    """
    Calendar browser view
    """
    implements(ICalendarView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def getPortalLanguage(self):
        ltool = getToolByName(self.context, 'portal_languages')
        lang = ltool.getPreferredLanguage()
        lang = lang[:2]
        if lang and lang != 'en':
            return lang

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()


