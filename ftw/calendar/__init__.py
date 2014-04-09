from zope.i18nmessageid import MessageFactory
import pkg_resources


calendarMessageFactory = MessageFactory('ftw.calendar')


try:
    pkg_resources.get_distribution('plone.app.event')
except pkg_resources.DistributionNotFound:
    HAS_PAEVENT = False
else:
    HAS_PAEVENT = True


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
